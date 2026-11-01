-- MobileWatch: read the gear sets out of GearSwap job files, on the phone.
--
-- GearSwap sets are code, not data (set_combine, gear.* helpers, the `empty`
-- token, sets built inside init_gear_sets()), so the files are RUN here, in a
-- sandbox standing in for GearSwap, and the finished `sets` table is walked.
-- This is the same approach as OmniWatch's sim Import Set.
--
-- Called from LuaGear.kt with three globals set:
--   __files  : array of { name = "Wormfood_Whm_Gear.lua", src = "<file text>" }
--              shared files (globals, items) first, then the job's own files
--   __main   : main job, e.g. "WHM"
--   __sub    : sub job, e.g. "SCH" (may be "")
--   __level  : main job level
-- and returns one string, a line per record:
--   S <tab> <set path>
--   I <tab> <slot> <tab> <item name> <tab> <bag> <tab> <aug> \31 <aug> ...
--   E <tab> <slot>                              (the set empties the slot)
--   W <tab> <message>                           (a file that would not load)
-- The phone never sees anything else from the file: there is no io, os or
-- network access in here.

local SLOTS = {
    main = 'main', sub = 'sub', range = 'range', ranged = 'range', ammo = 'ammo',
    head = 'head', neck = 'neck',
    ear1 = 'left_ear', ear2 = 'right_ear', left_ear = 'left_ear', right_ear = 'right_ear',
    lear = 'left_ear', rear = 'right_ear',
    body = 'body', hands = 'hands',
    ring1 = 'left_ring', ring2 = 'right_ring', left_ring = 'left_ring', right_ring = 'right_ring',
    lring = 'left_ring', rring = 'right_ring',
    back = 'back', waist = 'waist', legs = 'legs', feet = 'feet',
}

local function slot_of(k)
    if type(k) ~= 'string' then return nil end
    return SLOTS[k:lower()]
end

-- One object that can be indexed, called, concatenated and measured any
-- number of levels deep, so state.X:options(...), M{...}, windower.ffxi...,
-- world.area:contains(...) and friends never stop a file loading.
local stub
stub = setmetatable({}, {
    __index = function() return stub end,
    __newindex = function() end,          -- state.Buff['x'] = ... must not stick
    __call = function() return stub end,
    __concat = function(a, b)
        return (type(a) == 'string' and a or '') .. (type(b) == 'string' and b or '')
    end,
    __tostring = function() return '' end,
    __len = function() return 0 end,
    __unm = function() return 0 end,
    __add = function() return 0 end, __sub = function() return 0 end,
    __mul = function() return 0 end, __div = function() return 0 end,
})

-- Any nested access makes an empty sub-table, so `sets.engaged.HighHaste = {...}`
-- works without sets.engaged existing first, as it does in GearSwap.
local function autoviv()
    return setmetatable({}, {
        __index = function(self, k)
            local v = autoviv()
            rawset(self, k, v)
            return v
        end,
    })
end

-- Unknown keys read as the stub, but anything assigned is kept and read back.
local function lenient(t)
    return setmetatable(t or {}, { __index = function() return stub end })
end

local EMPTY = { __mw_empty = true }

local function make_env()
    local env = {}
    env._G = env
    for _, k in ipairs({ 'pairs', 'ipairs', 'type', 'tostring', 'tonumber', 'pcall',
                         'xpcall', 'select', 'next', 'setmetatable', 'getmetatable',
                         'rawget', 'rawset', 'rawequal', 'error', 'assert' }) do
        env[k] = _G[k]
    end
    env.unpack = table.unpack or unpack
    env.table, env.string, env.math = table, string, math
    env.print = function() end
    env.load = function() return function() end end
    env.loadstring = env.load
    env.require = function() return lenient({}) end

    env.sets = autoviv()
    env.gear = autoviv()
    env.empty = EMPTY

    -- GearSwap's set_combine: later sets win, slot by slot. ear1 and
    -- left_ear are the same slot, so they are merged under one name or the
    -- later piece would not replace the earlier one. Only the slots are
    -- carried: a set built from sets.precast.WS must not drag in WS.Acc and
    -- every other set hung off it as phantom copies of its own.
    env.set_combine = function(...)
        local out = {}
        for i = 1, select('#', ...) do
            local t = select(i, ...)
            if type(t) == 'table' then
                for k, v in pairs(t) do
                    local s = slot_of(k)
                    if s then
                        for other, canon in pairs(SLOTS) do
                            if canon == s and other ~= s then out[other] = nil end
                        end
                        out[s] = v
                    end
                end
            end
        end
        return out
    end

    local function ctor() return stub end
    env.M, env.S, env.T, env.L, env.Q = ctor, ctor, ctor, ctor, ctor
    env.include = function() end
    env.send_command = function() end
    env.add_to_chat = function() end
    env.windower = stub
    env.state = lenient({})
    env.data = stub
    env.classes = stub
    env.info = lenient({})
    env.buffactive = setmetatable({}, { __index = function() return nil end })

    local sub = __sub or ''
    env.player = lenient({
        name = '', main_job = __main, sub_job = sub,
        main_job_full = '', sub_job_full = '',
        main_job_level = tonumber(__level) or 99,
        sub_job_level = math.floor((tonumber(__level) or 99) / 2),
        status = 'Idle', hpp = 100, mpp = 100, tp = 0,
        equipment = lenient({}), buffs = {}, inventory = lenient({}),
    })
    env.world = lenient({ area = '', weather_element = '', day_element = '' })
    env.alliance = lenient({})
    env.pet = lenient({ isvalid = false })

    setmetatable(env, { __index = function() return stub end })
    return env
end

-- ── the walk ─────────────────────────────────────────────────────────────

local function path_key(k)
    if type(k) == 'string' and k:match('^[%a_][%w_]*$') then return '.' .. k end
    if type(k) == 'string' then return "['" .. k .. "']" end
    return '[' .. tostring(k) .. ']'
end

local function clean(s)
    return (tostring(s or ''):gsub('[\t\r\n\30\31]', ' '))
end

local function item_line(slot, ref)
    if ref == EMPTY or (type(ref) == 'table' and rawget(ref, '__mw_empty')) then
        return 'E\t' .. slot
    end
    if type(ref) == 'string' then
        if ref == '' then return nil end
        return 'I\t' .. slot .. '\t' .. clean(ref) .. '\t\t'
    end
    if type(ref) == 'table' then
        local name = rawget(ref, 'name') or rawget(ref, 'en') or rawget(ref, 'enl')
        if type(name) ~= 'string' or name == '' then return nil end
        local augs = {}
        local a = rawget(ref, 'augments')
        if type(a) == 'table' then
            for _, s in ipairs(a) do
                if type(s) == 'string' and s ~= '' then augs[#augs + 1] = clean(s) end
            end
        end
        local bag = rawget(ref, 'bag')
        return 'I\t' .. slot .. '\t' .. clean(name) .. '\t' ..
            (type(bag) == 'string' and clean(bag) or '') .. '\t' .. table.concat(augs, '\31')
    end
    return nil
end

local function sorted_keys(t)
    local ks = {}
    for k in pairs(t) do ks[#ks + 1] = k end
    table.sort(ks, function(a, b) return tostring(a):lower() < tostring(b):lower() end)
    return ks
end

local out = {}

local function walk(node, path, depth, onpath)
    if depth > 10 or onpath[node] then return end
    onpath[node] = true
    local lines = {}
    local seen_slot = {}
    for _, k in ipairs(sorted_keys(node)) do
        local s = slot_of(k)
        if s and not seen_slot[s] then
            local l = item_line(s, rawget(node, k))
            if l then lines[#lines + 1] = l; seen_slot[s] = true end
        end
    end
    if #lines > 0 then
        out[#out + 1] = 'S\t' .. path
        for _, l in ipairs(lines) do out[#out + 1] = l end
    end
    for _, k in ipairs(sorted_keys(node)) do
        local v = rawget(node, k)
        if not slot_of(k) and type(v) == 'table' and v ~= EMPTY then
            walk(v, path .. path_key(k), depth + 1, onpath)
        end
    end
    onpath[node] = nil
end

-- ── run ──────────────────────────────────────────────────────────────────

local env = make_env()
for _, f in ipairs(__files) do
    local chunk, err = load(f.src, '=' .. f.name, 't', env)
    if not chunk then
        out[#out + 1] = 'W\t' .. clean(err)
    else
        local ok, rerr = pcall(chunk)
        if not ok then out[#out + 1] = 'W\t' .. clean(f.name .. ': ' .. tostring(rerr)) end
    end
end

-- Sets are usually built inside these rather than at file scope. Each is
-- guarded: a setup function that trips over something we stubbed must not
-- cost the sets that come after it.
for _, fn in ipairs({ 'job_setup', 'user_setup', 'user_job_setup', 'character_user_job_setup',
                      'get_sets', 'init_gear_sets', 'user_init_gear_sets',
                      'job_init_gear_sets', 'init_sets' }) do
    local f = rawget(env, fn)
    if type(f) == 'function' then pcall(f) end
end

walk(rawget(env, 'sets'), 'sets', 0, {})
return table.concat(out, '\n')
