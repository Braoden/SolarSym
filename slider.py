from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectSlider
from objects import Objects
from math import log10

class Slider:

    def __init__(self):
            """Create a slider UI to control time_scale dynamically"""
            # Create a frame to hold the slider and label
            self.time_scale_frame = DirectFrame(
                frameColor=(0, 0, 0, 0.8),
                frameSize=(-0.3, 0.3, -0.2, 0.2),
                pos=(-1.5, 0, 0.75)
            )
            
            # Label for "Time Scale"
            DirectLabel(
                parent=self.time_scale_frame,
                text="Time Scale",
                scale=0.05,
                pos=(0, 0, 0.06),
                textMayChange=False
            )
            
            # Label to display current value (will update dynamically)
            self.time_scale_value_label = DirectLabel(
                parent=self.time_scale_frame,
                text=f"{int(Objects.time_scale)}x",
                scale=0.04,
                pos=(0, 0, -0.08),
                frameSize=(-2.5, 2.5, -0.4, 0.8), 
                textMayChange=True
            )
            
            # Create slider
            # Using logarithmic scale: slider value 0-100 maps to time_scale 1 to 1e6
            # Default position corresponds to current time_scale (1e5)
            initial_value = self.time_scale_to_slider_value(Objects.time_scale)
            
            self.time_scale_slider = DirectSlider(
                parent=self.time_scale_frame,
                range=(0, 100),
                value=initial_value,
                pageSize=4,
                command=self.on_time_scale_change,
                scale=0.25,
                pos=(0, 0, 0)
            )
        
    def time_scale_to_slider_value(self, time_scale):
        """Convert time_scale to slider value (logarithmic scale: 1 to 1e6)"""
        if time_scale <= 0:
            return 0
        log_value = log10(max(time_scale, 1))
        # Normalize to 0-100 range (log goes from 0 to 6 for 1 to 1e6)
        slider_value = (log_value / 6.0) * 100
        return max(0, min(100, slider_value))
    
    def slider_value_to_time_scale(self, slider_value):
        """Convert slider value to time_scale (logarithmic scale: 1 to 1e6)"""
        # Normalize slider value (0-100) to log range (0 to 6)
        log_value = (slider_value / 100.0) * 6.0
        # Convert back to linear scale
        time_scale = 10 ** log_value
        return max(1, time_scale)
    
    def on_time_scale_change(self):
        """Callback function when slider is moved"""
        # Convert slider value to time_scale
        value = self.time_scale_slider['value']
        new_time_scale = self.slider_value_to_time_scale(value)
        
        # Update the class variable (affects all objects)
        Objects.time_scale = new_time_scale
        
        # Update the display label (rounded to integer)
        self.time_scale_value_label["text"] = f"{int(new_time_scale) + 1}x"
