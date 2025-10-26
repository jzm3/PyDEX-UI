#!/usr/bin/env python3
"""
PyDEX-UI - 科幻风格系统监控和终端模拟器
基于Python 3.13和Dear PyGui构建
"""

import dearpygui.dearpygui as dpg
import psutil
import time
import subprocess
import threading
import platform
from datetime import datetime

class PyDexUI:
    def __init__(self):
        # 初始化数据存储
        self.cpu_history = []
        self.memory_history = []
        self.network_history = []
        self.disk_history = []
        
        # 网络统计
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()
        
        # 磁盘统计
        self.last_disk_io = psutil.disk_io_counters()
        self.last_disk_time = time.time()
        
        # 初始化GUI
        self.setup_gui()
        
    def setup_gui(self):
        """设置GUI界面"""
        dpg.create_context()
        
        # 创建科幻风格主题
        self.create_scifi_theme()
        
        # 创建视口
        dpg.create_viewport(
            title='PyDEX-UI - Sci-Fi System Monitor', 
            width=1200, 
            height=800,
            resizable=True,
            vsync=True
        )
        
        # 创建主窗口
        with dpg.window(
            tag="Primary Window",
            label="PyDEX-UI",
            no_title_bar=True,
            no_move=True,
            no_resize=True,
            no_collapse=True,
            no_scrollbar=True
        ):
            # 创建标签页
            with dpg.tab_bar(tag="Main Tab Bar"):
                # 系统监控标签页
                with dpg.tab(label="System Monitor"):
                    self.create_system_monitor_tab()
                
                # 终端标签页
                with dpg.tab(label="Terminal"):
                    self.create_terminal_tab()
                
                # 进程监控标签页
                with dpg.tab(label="Processes"):
                    self.create_process_monitor_tab()
            
            # 底部状态栏
            self.create_status_bar()
        
        # 设置视口
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        
        # 设置定时器更新数据
        dpg.set_frame_callback(1, self.update_all_data)
    
    def create_scifi_theme(self):
        """创建科幻风格主题"""
        with dpg.theme() as self.scifi_theme:
            with dpg.theme_component(dpg.mvAll):
                # 深色背景
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (10, 10, 20, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (15, 15, 25, 255))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (20, 20, 30, 240))
                
                # 文字颜色 - 青色/蓝色调
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (100, 100, 150, 255))
                
                # 边框和线条 - 亮蓝色
                dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 200, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_PlotLines, (0, 200, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (0, 200, 255, 255))
                
                # 按钮和交互元素
                dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 100, 150, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 150, 200, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 200, 255, 255))
                
                # 框架和标题
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (30, 30, 60, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (40, 40, 80, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (50, 50, 100, 255))
                
                # 标题栏
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (10, 10, 30, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (20, 20, 50, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (10, 10, 30, 200))
                
                # 标签页
                dpg.add_theme_color(dpg.mvThemeCol_Tab, (20, 20, 50, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (30, 30, 80, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TabActive, (40, 40, 100, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, (15, 15, 35, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, (25, 25, 60, 255))
                
                # 滑块
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (0, 200, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (0, 255, 255, 255))
                
                # 复选框
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (0, 255, 255, 255))
                
                # 分隔线
                dpg.add_theme_color(dpg.mvThemeCol_Separator, (0, 150, 200, 255))
                dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered, (0, 200, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive, (0, 255, 255, 255))
        
        # 应用主题
        dpg.bind_theme(self.scifi_theme)
    
    def create_system_monitor_tab(self):
        """创建系统监控标签页"""
        # 顶部系统信息栏
        with dpg.group(horizontal=True):
            # CPU使用率
            with dpg.child_window(width=300, height=150):
                dpg.add_text("CPU", color=(0, 255, 255))
                dpg.add_progress_bar(label="CPU Usage", default_value=0.5, 
                                    overlay="50%", tag="cpu_usage_bar")
                dpg.add_text("Cores: ", tag="cpu_cores")
                dpg.add_text("Frequency: ", tag="cpu_freq")
            
            # 内存使用率
            with dpg.child_window(width=300, height=150):
                dpg.add_text("Memory", color=(0, 255, 255))
                dpg.add_progress_bar(label="Memory Usage", default_value=0.5,
                                    overlay="50%", tag="memory_usage_bar")
                dpg.add_text("Used: ", tag="memory_used")
                dpg.add_text("Available: ", tag="memory_available")
            
            # 磁盘使用率
            with dpg.child_window(width=300, height=150):
                dpg.add_text("Disk", color=(0, 255, 255))
                dpg.add_progress_bar(label="Disk Usage", default_value=0.5,
                                    overlay="50%", tag="disk_usage_bar")
                dpg.add_text("Used: ", tag="disk_used")
                dpg.add_text("Free: ", tag="disk_free")
            
            # 网络状态
            with dpg.child_window(width=300, height=150):
                dpg.add_text("Network", color=(0, 255, 255))
                dpg.add_text("Upload: ", tag="network_upload")
                dpg.add_text("Download: ", tag="network_download")
                dpg.add_text("Connections: ", tag="network_connections")
        
        # 图表区域
        with dpg.group(horizontal=True):
            # CPU历史图表
            with dpg.child_window(width=600, height=300):
                dpg.add_text("CPU Usage History", color=(0, 255, 255))
                with dpg.plot(label="CPU History", height=250, width=-1):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="Time", no_gridlines=True)
                    y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Percentage", no_gridlines=True)
                    # 移除color参数，使用默认颜色
                    dpg.add_line_series([], [], label="CPU %", parent=y_axis, tag="cpu_plot")
            
            # 内存历史图表
            with dpg.child_window(width=600, height=300):
                dpg.add_text("Memory Usage History", color=(0, 255, 255))
                with dpg.plot(label="Memory History", height=250, width=-1):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="Time", no_gridlines=True)
                    y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Percentage", no_gridlines=True)
                    # 移除color参数，使用默认颜色
                    dpg.add_line_series([], [], label="Memory %", parent=y_axis, tag="memory_plot")
        
        # 底部图表
        with dpg.group(horizontal=True):
            # 网络历史图表
            with dpg.child_window(width=600, height=300):
                dpg.add_text("Network I/O History", color=(0, 255, 255))
                with dpg.plot(label="Network History", height=250, width=-1):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="Time", no_gridlines=True)
                    y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="KB/s", no_gridlines=True)
                    # 移除color参数，使用默认颜色
                    dpg.add_line_series([], [], label="Upload", parent=y_axis, tag="network_upload_plot")
                    dpg.add_line_series([], [], label="Download", parent=y_axis, tag="network_download_plot")
            
            # 磁盘I/O历史图表
            with dpg.child_window(width=600, height=300):
                dpg.add_text("Disk I/O History", color=(0, 255, 255))
                with dpg.plot(label="Disk History", height=250, width=-1):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="Time", no_gridlines=True)
                    y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="KB/s", no_gridlines=True)
                    # 移除color参数，使用默认颜色
                    dpg.add_line_series([], [], label="Read", parent=y_axis, tag="disk_read_plot")
                    dpg.add_line_series([], [], label="Write", parent=y_axis, tag="disk_write_plot")
    
    def create_terminal_tab(self):
        """创建终端标签页"""
        with dpg.group(horizontal=True):
            # 终端输出区域
            with dpg.child_window(width=-1, height=-32):
                dpg.add_input_text(
                    multiline=True,
                    readonly=True,
                    tag="terminal_output",
                    width=-1,
                    height=-1,
                    tab_input=True
                )
            
        # 终端输入区域
        with dpg.group(horizontal=True):
            dpg.add_text("$>", color=(0, 255, 255))
            dpg.add_input_text(
                hint="Enter command...",
                tag="terminal_input",
                width=-1,
                callback=self.execute_command,
                on_enter=True
            )
    
    def create_process_monitor_tab(self):
        """创建进程监控标签页"""
        with dpg.child_window(width=-1, height=-1):
            dpg.add_text("Running Processes", color=(0, 255, 255))
            dpg.add_separator()
            
            # 进程列表
            with dpg.table(
                header_row=True,
                borders_innerH=True,
                borders_outerH=True,
                borders_innerV=True,
                borders_outerV=True,
                row_background=True,
                resizable=True,
                reorderable=True,
                hideable=True,
                sortable=True,
                tag="process_table"
            ):
                dpg.add_table_column(label="PID", init_width_or_weight=0.1)
                dpg.add_table_column(label="Name", init_width_or_weight=0.3)
                dpg.add_table_column(label="Status", init_width_or_weight=0.1)
                dpg.add_table_column(label="CPU %", init_width_or_weight=0.1)
                dpg.add_table_column(label="Memory %", init_width_or_weight=0.1)
                dpg.add_table_column(label="Memory (MB)", init_width_or_weight=0.15)
                dpg.add_table_column(label="User", init_width_or_weight=0.15)
    
    def create_status_bar(self):
        """创建底部状态栏"""
        with dpg.group(horizontal=True):
            dpg.add_text("System: ", tag="system_info")
            dpg.add_text(" | Uptime: ", tag="system_uptime")
            dpg.add_text(" | Time: ", tag="current_time")
            dpg.add_text(" | PyDEX-UI v1.0", tag="app_version")
    
    def update_all_data(self, sender, app_data):
        """更新所有系统数据"""
        self.update_cpu_info()
        self.update_memory_info()
        self.update_disk_info()
        self.update_network_info()
        self.update_process_list()
        self.update_status_bar()
        
        # 设置下一帧更新
        dpg.set_frame_callback(dpg.get_frame_count() + 30, self.update_all_data)
    
    def update_cpu_info(self):
        """更新CPU信息"""
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count()
        
        # 更新进度条和文本
        dpg.set_value("cpu_usage_bar", cpu_percent / 100)
        dpg.configure_item("cpu_usage_bar", overlay=f"{cpu_percent:.1f}%")
        dpg.set_value("cpu_cores", f"Cores: {cpu_count} (Logical: {psutil.cpu_count(logical=True)})")
        
        if cpu_freq:
            dpg.set_value("cpu_freq", f"Frequency: {cpu_freq.current:.0f} MHz")
        
        # 更新历史图表
        self.cpu_history.append(cpu_percent)
        if len(self.cpu_history) > 100:
            self.cpu_history.pop(0)
        
        if len(self.cpu_history) > 1:
            dpg.set_value("cpu_plot", [list(range(len(self.cpu_history))), list(self.cpu_history)])
    
    def update_memory_info(self):
        """更新内存信息"""
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # 更新进度条和文本
        dpg.set_value("memory_usage_bar", memory_percent / 100)
        dpg.configure_item("memory_usage_bar", overlay=f"{memory_percent:.1f}%")
        
        used_gb = memory.used / (1024 ** 3)
        available_gb = memory.available / (1024 ** 3)
        total_gb = memory.total / (1024 ** 3)
        
        dpg.set_value("memory_used", f"Used: {used_gb:.1f} GB / {total_gb:.1f} GB")
        dpg.set_value("memory_available", f"Available: {available_gb:.1f} GB")
        
        # 更新历史图表
        self.memory_history.append(memory_percent)
        if len(self.memory_history) > 100:
            self.memory_history.pop(0)
            
        if len(self.memory_history) > 1:
            dpg.set_value("memory_plot", [list(range(len(self.memory_history))), list(self.memory_history)])
    
    def update_disk_info(self):
        """更新磁盘信息"""
        try:
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # 更新进度条和文本
            dpg.set_value("disk_usage_bar", disk_percent / 100)
            dpg.configure_item("disk_usage_bar", overlay=f"{disk_percent:.1f}%")
            
            used_gb = disk.used / (1024 ** 3)
            free_gb = disk.free / (1024 ** 3)
            total_gb = disk.total / (1024 ** 3)
            
            dpg.set_value("disk_used", f"Used: {used_gb:.1f} GB / {total_gb:.1f} GB")
            dpg.set_value("disk_free", f"Free: {free_gb:.1f} GB")
            
            # 更新磁盘I/O图表
            current_disk_io = psutil.disk_io_counters()
            current_time = time.time()
            
            if self.last_disk_io and current_disk_io:
                time_diff = current_time - self.last_disk_time
                read_speed = (current_disk_io.read_bytes - self.last_disk_io.read_bytes) / time_diff / 1024
                write_speed = (current_disk_io.write_bytes - self.last_disk_io.write_bytes) / time_diff / 1024
                
                self.disk_history.append((read_speed, write_speed))
                if len(self.disk_history) > 100:
                    self.disk_history.pop(0)
                
                if len(self.disk_history) > 1:
                    times = list(range(len(self.disk_history)))
                    reads = [point[0] for point in self.disk_history]
                    writes = [point[1] for point in self.disk_history]
                    
                    dpg.set_value("disk_read_plot", [times, reads])
                    dpg.set_value("disk_write_plot", [times, writes])
            
            self.last_disk_io = current_disk_io
            self.last_disk_time = current_time
            
        except Exception as e:
            print(f"Error updating disk info: {e}")
    
    def update_network_info(self):
        """更新网络信息"""
        try:
            current_net_io = psutil.net_io_counters()
            current_time = time.time()
            
            if self.last_net_io and current_net_io:
                time_diff = current_time - self.last_net_time
                upload_speed = (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / time_diff / 1024
                download_speed = (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / time_diff / 1024
                
                # 更新网络速度文本
                dpg.set_value("network_upload", f"Upload: {upload_speed:.1f} KB/s")
                dpg.set_value("network_download", f"Download: {download_speed:.1f} KB/s")
                
                # 更新网络连接数
                try:
                    connections = len(psutil.net_connections())
                    dpg.set_value("network_connections", f"Connections: {connections}")
                except:
                    dpg.set_value("network_connections", "Connections: N/A")
                
                # 更新网络I/O图表
                self.network_history.append((upload_speed, download_speed))
                if len(self.network_history) > 100:
                    self.network_history.pop(0)
                
                if len(self.network_history) > 1:
                    times = list(range(len(self.network_history)))
                    uploads = [point[0] for point in self.network_history]
                    downloads = [point[1] for point in self.network_history]
                    
                    dpg.set_value("network_upload_plot", [times, uploads])
                    dpg.set_value("network_download_plot", [times, downloads])
            
            self.last_net_io = current_net_io
            self.last_net_time = current_time
            
        except Exception as e:
            print(f"Error updating network info: {e}")
    
    def update_process_list(self):
        """更新进程列表"""
        try:
            # 清除现有进程行
            if dpg.does_item_exist("process_table"):
                dpg.delete_item("process_table", children_only=True)
            
            # 获取进程信息
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent', 'memory_info', 'username']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            # 按CPU使用率排序
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            # 只显示前50个进程
            for proc in processes[:50]:
                with dpg.table_row(parent="process_table"):
                    dpg.add_text(str(proc['pid']))
                    dpg.add_text(proc['name'] or "N/A")
                    dpg.add_text(proc['status'] or "N/A")
                    dpg.add_text(f"{proc['cpu_percent'] or 0:.1f}" if proc['cpu_percent'] else "0.0")
                    dpg.add_text(f"{proc['memory_percent'] or 0:.1f}" if proc['memory_percent'] else "0.0")
                    
                    memory_mb = proc['memory_info'].rss / (1024 * 1024) if proc['memory_info'] else 0
                    dpg.add_text(f"{memory_mb:.1f}")
                    
                    dpg.add_text(proc['username'] or "N/A")
                    
        except Exception as e:
            print(f"Error updating process list: {e}")
    
    def update_status_bar(self):
        """更新状态栏"""
        # 系统信息
        system = f"{platform.system()} {platform.release()}"
        dpg.set_value("system_info", f"System: {system}")
        
        # 系统运行时间
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
        dpg.set_value("system_uptime", f" | Uptime: {uptime_str}")
        
        # 当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dpg.set_value("current_time", f" | Time: {current_time}")
    
    def execute_command(self, sender, app_data):
        """执行终端命令"""
        command = dpg.get_value("terminal_input")
        dpg.set_value("terminal_input", "")
        
        if not command.strip():
            return
        
        # 添加命令到终端输出
        current_output = dpg.get_value("terminal_output")
        new_output = f"{current_output}\n$ {command}"
        dpg.set_value("terminal_output", new_output)
        
        # 在新线程中执行命令
        thread = threading.Thread(target=self._run_command, args=(command,))
        thread.daemon = True
        thread.start()
    
    def _run_command(self, command):
        """在新线程中运行命令"""
        try:
            # 创建子进程执行命令
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # 实时读取输出
            for line in iter(process.stdout.readline, ''):
                if line:
                    # 在主线程中更新GUI
                    current_output = dpg.get_value("terminal_output")
                    dpg.set_value("terminal_output", current_output + line)
            
            process.stdout.close()
            return_code = process.wait()
            
            # 添加命令完成提示
            if return_code == 0:
                completion_text = f"\n[Command completed with exit code {return_code}]"
            else:
                completion_text = f"\n[Command failed with exit code {return_code}]"
            
            current_output = dpg.get_value("terminal_output")
            dpg.set_value("terminal_output", current_output + completion_text)
            
        except Exception as e:
            error_msg = f"\nError executing command: {str(e)}"
            current_output = dpg.get_value("terminal_output")
            dpg.set_value("terminal_output", current_output + error_msg)
    
    def run(self):
        """运行应用"""
        dpg.start_dearpygui()
    
    def cleanup(self):
        """清理资源"""
        dpg.destroy_context()

def main():
    """主函数"""
    app = PyDexUI()
    try:
        app.run()
    except KeyboardInterrupt:
        print("Shutting down PyDEX-UI...")
    finally:
        app.cleanup()

if __name__ == "__main__":
    main()