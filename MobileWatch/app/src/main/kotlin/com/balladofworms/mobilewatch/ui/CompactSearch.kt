package com.balladofworms.mobilewatch.ui

import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LocalTextStyle
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.balladofworms.mobilewatch.ui.theme.TextMuted

/**
 * The search box, shorter than a standard outlined field (44 dp instead of 56) but drawn
 * with the same outline, colours and icons -- the standard one pads its text with 16 dp above
 * and below, which is what made it tall.
 */
@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
internal fun CompactSearchField(
    value: String,
    onValueChange: (String) -> Unit,
    placeholder: String,
    modifier: Modifier = Modifier
) {
    val interaction = remember { MutableInteractionSource() }
    val colors = OutlinedTextFieldDefaults.colors()
    val shape = RoundedCornerShape(12.dp)
    BasicTextField(
        value = value,
        onValueChange = onValueChange,
        modifier = modifier.height(44.dp),
        singleLine = true,
        textStyle = LocalTextStyle.current.copy(color = MaterialTheme.colorScheme.onSurface, fontSize = 15.sp),
        cursorBrush = SolidColor(MaterialTheme.colorScheme.primary),
        interactionSource = interaction
    ) { inner ->
        OutlinedTextFieldDefaults.DecorationBox(
            value = value,
            innerTextField = inner,
            enabled = true,
            singleLine = true,
            visualTransformation = VisualTransformation.None,
            interactionSource = interaction,
            placeholder = { Text(placeholder, fontSize = 15.sp, maxLines = 1, overflow = TextOverflow.Ellipsis) },
            leadingIcon = { Icon(Icons.Filled.Search, null) },
            trailingIcon = {
                if (value.isNotEmpty()) IconButton(onClick = { onValueChange("") }) {
                    Icon(Icons.Filled.Close, "Clear", tint = TextMuted)
                }
            },
            colors = colors,
            contentPadding = PaddingValues(horizontal = 4.dp, vertical = 0.dp),
            container = {
                OutlinedTextFieldDefaults.ContainerBox(
                    enabled = true, isError = false, interactionSource = interaction,
                    colors = colors, shape = shape)
            }
        )
    }
}
