from i3pystatus import IntervalModule
from .utils import gpu


class GPUTemperature(IntervalModule):
    """
    Shows GPU temperature

    Currently Nvidia only and nvidia-smi required

    .. rubric:: Available formatters

    * `{temp}`       — the temperature in integer degrees celsius
    """

    settings = (
        ("format", "format string used for output. {temp} is the temperature in integer degrees celsius"),
        ("display_if", "snippet that gets evaluated. if true, displays the module output"),
        "color",
        "alert_temp",
        "alert_color",
    )
    format = "{temp} °C"
    color = "#FFFFFF"
    alert_temp = 90
    alert_color = "#FF0000"

    def run(self):
        gpu_query = gpu.query_nvidia_smi()
        temp = gpu_query.temp
        percent_fan = gpu_query.percent_fan
        total_mem = gpu_query.total_mem
        avail_mem = gpu_query.avail_mem
        used_mem = gpu_query.used_mem
        usage_gpu = gpu_query.usage_gpu
        usage_mem = gpu_query.usage_mem
        temp_alert = temp is None or temp >= self.alert_temp

        self.output = {
            "full_text": self.format.format(temp=temp, percent_fan=percent_fan, total_mem=total_mem,
                                            avail_mem=avail_mem, used_mem=used_mem,
                                            usage_gpu=usage_gpu, usage_mem=usage_mem),
            "color": self.color if not temp_alert else self.alert_color,
        }
