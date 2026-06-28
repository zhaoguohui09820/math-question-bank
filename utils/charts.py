import json
import datetime

def generate_heatmap_html(daily_activity):
    today = datetime.date.today()
    start_date = datetime.date(2026, 1, 1)
    
    if today < start_date:
        today = datetime.date(2026, 12, 31)
        
    start_sunday = start_date - datetime.timedelta(days=(start_date.weekday() + 1) % 7)
    
    weeks = []
    current_date = start_sunday
    while current_date <= today:
        week = []
        for _ in range(7):
            if current_date < start_date or current_date > today:
                week.append(None)
            else:
                week.append(current_date)
            current_date += datetime.timedelta(days=1)
        weeks.append(week)
        
    month_names = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    months_html = '<div style="display: flex; font-size: 12px; color: #8b949e; height: 20px; align-items: flex-end; padding-bottom: 4px;">'
    current_month = None
    for week in weeks:
        day = next((d for d in week if d is not None), None)
        if day and day.month != current_month:
            months_html += f'<div style="width: 18px; overflow: visible; white-space: nowrap; color: #8b949e;">{month_names[day.month-1]}</div>'
            current_month = day.month
        else:
            months_html += f'<div style="width: 18px;"></div>'
    months_html += '</div>'
    
    grid_html = '<div class="heatmap-grid">'
    for week in weeks:
        grid_html += '<div class="heatmap-col">'
        for day in week:
            if day is None:
                grid_html += '<div class="heatmap-cell hidden"></div>'
            else:
                date_str = day.isoformat()
                count = daily_activity.get(date_str, 0)
                if count == 0: level = 0
                elif count <= 2: level = 1
                elif count <= 5: level = 2
                elif count <= 10: level = 3
                else: level = 4
                
                if count > 0:
                    title = f"{date_str} 录入/修改了 {count} 次题目"
                else:
                    title = f"{date_str} 无记录"
                grid_html += f'<div class="heatmap-cell" data-level="{level}" title="{title}"></div>'
        grid_html += '</div>'
    grid_html += '</div>'
    
    html = """
    <style>
    body { margin: 0; padding: 0; background: #0d1117; }
    .heatmap-container {
        display: flex;
        flex-direction: column;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        background:
            radial-gradient(circle at 92% 8%, rgba(88, 166, 255, 0.10), transparent 12rem),
            linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        color: #c9d1d9;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(48, 54, 61, 0.9);
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.3);
        width: 100%;
        height: 300px;
        box-sizing: border-box;
        overflow: hidden;
        margin-bottom: 0px;
        transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease;
        animation: chartFadeUp 0.4s ease both;
    }
    @keyframes chartFadeUp {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .heatmap-container:hover {
        transform: translateY(-2px);
        border-color: rgba(88, 166, 255, 0.3);
        box-shadow: 0 18px 44px rgba(0, 0, 0, 0.4);
    }
    .heatmap-scroll-area {
        display: flex;
        flex: 1;
        overflow-x: auto;
        overflow-y: hidden;
        padding-top: 35px;
        padding-bottom: 5px;
    }
    .heatmap-scroll-area::-webkit-scrollbar {
        height: 8px;
    }
    .heatmap-scroll-area::-webkit-scrollbar-track {
        background: rgba(48, 54, 61, 0.5);
        border-radius: 4px;
    }
    .heatmap-scroll-area::-webkit-scrollbar-thumb {
        background: rgba(72, 79, 88, 0.6);
        border-radius: 4px;
    }
    .heatmap-scroll-area::-webkit-scrollbar-thumb:hover {
        background: rgba(139, 148, 158, 0.7);
    }
    .heatmap-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: -10px;
        color: #c9d1d9;
    }
    .heatmap-grid {
        display: flex;
        gap: 4px;
    }
    .heatmap-col {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .heatmap-cell {
        width: 14px;
        height: 14px;
        border-radius: 3px;
        background-color: rgba(48, 54, 61, 0.8);
        position: relative;
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }
    .heatmap-cell:not(.hidden):hover {
        transform: scale(1.18);
        box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.4);
    }
    .heatmap-cell[data-level="1"] { background-color: rgba(88, 166, 255, 0.4); }
    .heatmap-cell[data-level="2"] { background-color: rgba(88, 166, 255, 0.65); }
    .heatmap-cell[data-level="3"] { background-color: #58a6ff; }
    .heatmap-cell[data-level="4"] { background-color: #1f6feb; }
    .heatmap-cell.hidden { background-color: transparent; pointer-events: none; }
    
    .heatmap-footer {
        display: flex;
        justify-content: flex-end;
        width: 100%;
        margin-top: 10px;
        font-size: 14px;
        color: #8b949e;
        align-items: center;
    }
    .legend {
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .legend-cell {
        width: 14px;
        height: 14px;
        border-radius: 3px;
    }
    .heatmap-tooltip {
        display: none;
        position: fixed;
        background-color: rgba(13, 17, 23, 0.95);
        color: #c9d1d9;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 13px;
        white-space: nowrap;
        z-index: 99999;
        pointer-events: none;
        border: 1px solid #30363d;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    }
    </style>
    <div class="heatmap-container">
        <div class="heatmap-title">🗓️ 活跃指标 (Active Days)</div>
        <div class="heatmap-scroll-area">
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 12px; color: #8b949e; margin-right: 8px; margin-top: 20px; position: sticky; left: 0; background-color: #0d1117; z-index: 2;">
                <div style="height: 14px; line-height: 14px; text-align: right;">一</div>
                <div style="height: 14px; line-height: 14px; text-align: right;">二</div>
                <div style="height: 14px; line-height: 14px; text-align: right;">三</div>
                <div style="height: 14px; line-height: 14px; text-align: right;">四</div>
                <div style="height: 14px; line-height: 14px; text-align: right;">五</div>
                <div style="height: 14px; line-height: 14px; text-align: right;">六</div>
                <div style="height: 14px; line-height: 14px; text-align: right;">日</div>
            </div>
            <div>
                """ + months_html + """
                """ + grid_html + """
            </div>
        </div>
        <div class="heatmap-footer">
            <div class="legend">
                少
                <div class="legend-cell" style="background-color: rgba(48,54,61,0.8);"></div>
                <div class="legend-cell" style="background-color: rgba(88,166,255,0.4);"></div>
                <div class="legend-cell" style="background-color: rgba(88,166,255,0.65);"></div>
                <div class="legend-cell" style="background-color: #58a6ff;"></div>
                <div class="legend-cell" style="background-color: #1f6feb;"></div>
                多
            </div>
        </div>
    </div>
    <div id="heatmap-tooltip" class="heatmap-tooltip"></div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var tooltip = document.getElementById('heatmap-tooltip');
            var cells = document.querySelectorAll('.heatmap-cell');
            cells.forEach(function(cell) {
                cell.addEventListener('mouseenter', function(e) {
                    var title = cell.getAttribute('title');
                    if (title) {
                        tooltip.textContent = title;
                        tooltip.style.display = 'block';
                        tooltip.style.left = (e.clientX + 10) + 'px';
                        tooltip.style.top = (e.clientY - tooltip.offsetHeight - 10) + 'px';
                    }
                });
                cell.addEventListener('mousemove', function(e) {
                    tooltip.style.left = (e.clientX + 10) + 'px';
                    tooltip.style.top = (e.clientY - tooltip.offsetHeight - 10) + 'px';
                });
                cell.addEventListener('mouseleave', function() {
                    tooltip.style.display = 'none';
                });
            });
        });
    </script>
    """
    return html

def _generate_activity_curve_html_legacy(hourly_activity_by_day):
    today = datetime.date.today()
    days_data = []
    for i in range(6, -1, -1):
        d = today - datetime.timedelta(days=i)
        date_str = d.isoformat()
        if i == 0:
            label = "今天"
        elif i == 1:
            label = "昨天"
        else:
            label = d.strftime("%m-%d")
            
        hourly_counts = [hourly_activity_by_day.get(date_str, {}).get(str(h).zfill(2), 0) for h in range(24)]
        days_data.append({
            "label": label,
            "date": date_str,
            "counts": hourly_counts
        })
        
    days_data_json = json.dumps(days_data)
    
    html = """
    <style>
        body { margin: 0; padding: 0; background: #0d1117; }
        @keyframes activityFadeUp {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .activity-card {
            position: relative;
            width: 100%;
            height: 260px;
            background:
                radial-gradient(circle at 88% 10%, rgba(0, 122, 255, 0.18), transparent 12rem),
                linear-gradient(180deg, #111722 0%, #0d1117 100%);
            border-radius: 12px;
            border: 1px solid rgba(48, 54, 61, 0.9);
            padding: 10px;
            box-sizing: border-box;
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.3);
            transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease;
            animation: activityFadeUp 0.4s ease both;
        }
        .activity-card:hover {
            transform: translateY(-2px);
            border-color: rgba(88, 166, 255, 0.3);
            box-shadow: 0 18px 44px rgba(0, 0, 0, 0.4);
        }
        .activity-header {
            position: absolute;
            top: 10px;
            left: 20px;
            right: 18px;
            z-index: 10;
            display: flex;
            align-items: center;
            gap: 14px;
            min-width: 0;
        }
        .activity-title {
            flex: 0 0 auto;
            color: #c9d1d9;
            font-size: 16px;
            font-weight: 700;
            white-space: nowrap;
        }
        .day-selector-shell {
            position: relative;
            flex: 1 1 auto;
            min-width: 160px;
            max-width: 460px;
            overflow-x: auto;
            overflow-y: hidden;
            background-color: rgba(255,255,255,0.055);
            padding: 3px;
            border-radius: 8px;
            scrollbar-width: thin;
            scrollbar-color: rgba(148, 163, 184, 0.45) transparent;
        }
        .day-selector-shell::-webkit-scrollbar {
            height: 5px;
        }
        .day-selector-shell::-webkit-scrollbar-track {
            background: transparent;
        }
        .day-selector-shell::-webkit-scrollbar-thumb {
            background: rgba(148, 163, 184, 0.45);
            border-radius: 999px;
        }
        #day-selector {
            position: relative;
            display: flex;
            gap: 6px;
            width: max-content;
            min-width: 100%;
        }
        .day-selector-indicator {
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 0;
            border-radius: 6px;
            background: linear-gradient(180deg, #2f3745 0%, #202733 100%);
            box-shadow: 0 6px 16px rgba(0,0,0,0.22), inset 0 1px 0 rgba(255,255,255,0.08);
            transform: translateX(0);
            transition: transform 0.24s cubic-bezier(.2,.8,.2,1), width 0.24s cubic-bezier(.2,.8,.2,1);
            z-index: 0;
            pointer-events: none;
        }
        .day-selector-btn {
            position: relative;
            z-index: 1;
            flex: 0 0 auto;
            padding: 3px 10px;
            min-width: 48px;
            border-radius: 6px;
            color: #8b949e;
            font-size: 12px;
            line-height: 18px;
            text-align: center;
            cursor: pointer;
            user-select: none;
            transition: color 0.18s ease, transform 0.18s ease;
        }
        .day-selector-btn:hover {
            color: #dbeafe;
        }
        .day-selector-btn.active {
            color: #ffffff;
            transform: translateY(-1px);
        }
        #activity-chart {
            width: 100%;
            height: 100%;
            transition: opacity 0.22s ease, transform 0.22s ease;
        }
    </style>
    <div class="activity-card">
        <div class="activity-header">
            <div class="activity-title">⏱️ 时段活动曲线 ⓘ</div>
            <div id="day-selector-shell" class="day-selector-shell" title="在这里滚动鼠标滚轮可左右切换日期条">
                <div id="day-selector">
                    <div id="day-selector-indicator" class="day-selector-indicator"></div>
                </div>
            </div>
        </div>
        <div id="activity-chart"></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
    <script>
        var daysData = """ + days_data_json + """;
        var myChart = null;
        
        function initChart() {
            var chartDom = document.getElementById('activity-chart');
            if (!chartDom) return;
            myChart = echarts.init(chartDom, 'dark');
            var currentDayIndex = 0;
            var hasRenderedActivityChart = false;
            var selectorShell = document.getElementById('day-selector-shell');
            var selector = document.getElementById('day-selector');
            var indicator = document.getElementById('day-selector-indicator');
            
            selectorShell.addEventListener('wheel', function(e) {
                if (Math.abs(e.deltaY) >= Math.abs(e.deltaX)) {
                    selectorShell.scrollLeft += e.deltaY;
                    e.preventDefault();
                }
            }, { passive: false });
            
            function moveDayIndicator(activeBtn) {
                if (!activeBtn) return;
                indicator.style.width = activeBtn.offsetWidth + 'px';
                indicator.style.transform = 'translateX(' + activeBtn.offsetLeft + 'px)';
                var leftEdge = activeBtn.offsetLeft;
                var rightEdge = leftEdge + activeBtn.offsetWidth;
                if (leftEdge < selectorShell.scrollLeft) {
                    selectorShell.scrollTo({ left: leftEdge - 8, behavior: 'smooth' });
                } else if (rightEdge > selectorShell.scrollLeft + selectorShell.clientWidth) {
                    selectorShell.scrollTo({ left: rightEdge - selectorShell.clientWidth + 8, behavior: 'smooth' });
                }
            }
            
            function refreshDayButtons(dayIndex) {
                selector.querySelectorAll('.day-selector-btn').forEach(function(btn) {
                    var isActive = Number(btn.dataset.index) === dayIndex;
                    btn.classList.toggle('active', isActive);
                    if (isActive) {
                        moveDayIndicator(btn);
                    }
                });
            }
            
            function buildDaySelector() {
                daysData.forEach(function(day, index) {
                    var btn = document.createElement('div');
                    btn.className = 'day-selector-btn';
                    btn.dataset.index = index;
                    btn.innerText = day.label;
                    btn.onclick = function() {
                        renderChart(index);
                    };
                    selector.appendChild(btn);
                });
                requestAnimationFrame(function() {
                    refreshDayButtons(currentDayIndex);
                });
            }
            
            function renderChart(dayIndex) {
                currentDayIndex = dayIndex;
                var dayInfo = daysData[dayIndex];
                var hourly_counts = dayInfo.counts;
                var max_val = Math.max(...hourly_counts);
                if (max_val === 0) max_val = 1;
                
                if (hasRenderedActivityChart) {
                    chartDom.style.opacity = '0.72';
                    chartDom.style.transform = 'translateX(14px)';
                }
                
                var data = [];
                for (var i = 0; i <= 23; i++) {
                    var count = hourly_counts[i];
                    var y = Math.sin((i - 6) / 24 * Math.PI * 2);
                    data.push([i, y, count]);
                }

                var option = {
                    backgroundColor: 'transparent',
                    grid: { top: 40, bottom: 20, left: 20, right: 20, containLabel: true },
                    xAxis: {
                        type: 'value',
                        min: 0, max: 23,
                        interval: 1,
                        axisLine: { show: false },
                        splitLine: { show: false },
                        axisTick: { show: false },
                        axisLabel: {
                            formatter: function (value) {
                                if(value === 0) return '00:00';
                                if(value === 3) return '03:00';
                                if(value === 6) return '06:00';
                                if(value === 9) return '09:00';
                                if(value === 12) return '12:00';
                                if(value === 15) return '15:00';
                                if(value === 18) return '18:00';
                                if(value === 21) return '21:00';
                                if(value === 23) return '23:59';
                                return '';
                            },
                            color: '#8b949e',
                            fontSize: 13,
                            fontFamily: 'monospace',
                            margin: 8
                        }
                    },
                    yAxis: {
                        type: 'value',
                        min: -1.2, max: 1.5,
                        show: false
                    },
                    series: [
                        {
                            type: 'line',
                            data: data.map(function (item) { return [item[0], item[1]]; }),
                            smooth: true,
                            symbol: 'none',
                            lineStyle: { color: '#30363d', width: 2 },
                            z: 2,
                            markLine: {
                                symbol: ['none', 'none'],
                                label: { show: false },
                                data: [
                                    { yAxis: 0, lineStyle: { type: 'dashed', color: '#30363d', width: 1 } }
                                ]
                            }
                        },
                        {
                            type: 'scatter',
                            data: data,
                            z: 4,
                            symbolSize: function (data) {
                                return 12 + (data[2] / max_val) * 16; 
                            },
                            itemStyle: {
                                color: function(params) {
                                    if (params.data[2] === 0) return 'rgba(88, 166, 255, 0.15)';
                                    var opacity = 0.5 + (params.data[2] / max_val) * 0.5;
                                    return 'rgba(88, 166, 255, ' + opacity + ')';
                                }
                            },
                            tooltip: {
                                formatter: function(params) {
                                    var h = params.value[0];
                                    var hStr1 = (h < 10 ? '0' + h : h) + ':00';
                                    var hStr2 = (h < 10 ? '0' + h : h) + ':59';
                                    return hStr1 + ' ~ ' + hStr2 + ' 录入/修改了 ' + params.value[2] + ' 次题目';
                                }
                            }
                        },
                        {
                            type: 'scatter',
                            data: [[6, 0, 0], [12, 1.2, 0], [18, 0, 0], [21, -0.7, 0]],
                            symbol: 'circle',
                            symbolSize: 0,
                            z: 3,
                            label: {
                                show: true,
                                formatter: function(params) {
                                    if (params.data[0] === 6) return '🌅';
                                    if (params.data[0] === 12) return '☀️';
                                    if (params.data[0] === 18) return '🌇';
                                    if (params.data[0] === 21) return '🌙';
                                    return '';
                                },
                                position: 'top',
                                distance: 14,
                                fontSize: 16
                            }
                        }
                    ],
                    tooltip: { 
                        trigger: 'item', 
                        backgroundColor: 'rgba(13, 17, 23, 0.9)', 
                        borderColor: '#30363d', 
                        textStyle: { color: '#c9d1d9' },
                        formatter: function(params) {
                            if (params.componentType === 'series' && params.seriesIndex === 1) {
                                var h = params.value[0];
                                var hStr1 = (h < 10 ? '0' + h : h) + ':00';
                                var hStr2 = (h < 10 ? '0' + h : h) + ':59';
                                return hStr1 + ' ~ ' + hStr2 + ' 录入/修改了 ' + params.value[2] + ' 次题目';
                            }
                        }
                    }
                };
                myChart.setOption(option, true);
                refreshDayButtons(dayIndex);
                requestAnimationFrame(function() {
                    chartDom.style.opacity = '1';
                    chartDom.style.transform = 'translateX(0)';
                });
                hasRenderedActivityChart = true;
            }
            
            buildDaySelector();
            renderChart(0);
            window.addEventListener('resize', function() {
                if (myChart) myChart.resize();
                refreshDayButtons(currentDayIndex);
            });
        }
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initChart);
        } else {
            setTimeout(initChart, 300);
        }
    </script>
    """
    return html

def generate_activity_curve_html(hourly_activity_by_day):
    today = datetime.date.today()
    days_data = []
    for i in range(6, -1, -1):
        d = today - datetime.timedelta(days=i)
        date_str = d.isoformat()
        if i == 0:
            label = "今天"
        elif i == 1:
            label = "昨天"
        else:
            label = d.strftime("%m-%d")
            
        hourly_counts = [hourly_activity_by_day.get(date_str, {}).get(str(h).zfill(2), 0) for h in range(24)]
        days_data.append({
            "label": label,
            "date": date_str,
            "counts": hourly_counts
        })

    timeline = []
    for day_index, day in enumerate(days_data):
        for hour, count in enumerate(day["counts"]):
            timeline.append({
                "dayIndex": day_index,
                "dayLabel": day["label"],
                "date": day["date"],
                "hour": hour,
                "count": count
            })

    days_data_json = json.dumps(days_data)
    timeline_json = json.dumps(timeline)
    default_start = max(0, len(timeline) - 24)
    default_end = max(23, len(timeline) - 1)

    html = """
    <style>
        body { margin: 0; padding: 0; background: #0d1117; }
        @keyframes activityFadeUp {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .activity-card {
            position: relative;
            width: 100%;
            height: 300px;
            background:
                radial-gradient(circle at 88% 10%, rgba(88, 166, 255, 0.10), transparent 12rem),
                linear-gradient(180deg, #161b22 0%, #0d1117 100%);
            border-radius: 12px;
            border: 1px solid rgba(48, 54, 61, 0.9);
            padding: 10px;
            box-sizing: border-box;
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.3);
            transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease;
            animation: activityFadeUp 0.4s ease both;
        }
        .activity-card:hover {
            transform: translateY(-2px);
            border-color: rgba(88, 166, 255, 0.3);
            box-shadow: 0 18px 44px rgba(0, 0, 0, 0.4);
        }
        .activity-header {
            position: absolute;
            top: 10px;
            left: 20px;
            right: 18px;
            z-index: 10;
            display: flex;
            align-items: center;
            gap: 14px;
            min-width: 0;
        }
        .activity-title {
            flex: 0 0 auto;
            color: #c9d1d9;
            font-size: 16px;
            font-weight: 700;
            white-space: nowrap;
        }
        .day-selector-shell {
            position: relative;
            flex: 0 1 560px;
            min-width: 160px;
            overflow-x: auto;
            overflow-y: hidden;
            background-color: rgba(255,255,255,0.055);
            padding: 3px;
            border-radius: 8px;
            scrollbar-width: thin;
            scrollbar-color: rgba(148, 163, 184, 0.45) transparent;
        }
        .day-selector-shell::-webkit-scrollbar {
            height: 5px;
        }
        .day-selector-shell::-webkit-scrollbar-track {
            background: transparent;
        }
        .day-selector-shell::-webkit-scrollbar-thumb {
            background: rgba(148, 163, 184, 0.45);
            border-radius: 999px;
        }
        #day-selector {
            position: relative;
            display: flex;
            gap: 6px;
            width: max-content;
            min-width: 100%;
        }
        .day-selector-indicator {
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 0;
            border-radius: 6px;
            background: linear-gradient(180deg, #2f3745 0%, #202733 100%);
            box-shadow: 0 6px 16px rgba(0,0,0,0.22), inset 0 1px 0 rgba(255,255,255,0.08);
            transform: translateX(0);
            transition: transform 0.24s cubic-bezier(.2,.8,.2,1), width 0.24s cubic-bezier(.2,.8,.2,1);
            z-index: 0;
            pointer-events: none;
        }
        .day-selector-btn {
            position: relative;
            z-index: 1;
            flex: 1 1 0;
            padding: 4px 10px;
            min-width: 54px;
            border-radius: 999px;
            color: #8b949e;
            font-size: 12px;
            line-height: 18px;
            text-align: center;
            cursor: pointer;
            user-select: none;
            transition: color 0.18s ease, transform 0.18s ease;
        }
        .day-selector-btn:hover {
            color: #58a6ff;
        }
        .day-selector-btn.active {
            color: #c9d1d9;
            transform: translateY(-0.5px);
        }
        #activity-chart {
            width: 100%;
            height: 100%;
            transition: opacity 0.22s ease, transform 0.22s ease;
        }
    </style>
    <div class="activity-card">
        <div class="activity-header">
            <div class="activity-title">⏱️ 时段活动曲线</div>
            <div id="day-selector-shell" class="day-selector-shell">
                <div id="day-selector">
                    <div id="day-selector-indicator" class="day-selector-indicator"></div>
                </div>
            </div>
        </div>
        <div id="activity-chart"></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
    <script>
        var daysData = """ + days_data_json + """;
        var timelineData = """ + timeline_json + """;
        var defaultStart = """ + str(default_start) + """;
        var defaultEnd = """ + str(default_end) + """;
        var myChart = null;
        
        function initChart() {
            var chartDom = document.getElementById('activity-chart');
            if (!chartDom) return;
            myChart = echarts.init(chartDom, 'dark');
            var currentDayIndex = daysData.length - 1;
            var hasRenderedActivityChart = false;
            var selector = document.getElementById('day-selector');
            var indicator = document.getElementById('day-selector-indicator');

            function moveDayIndicator(activeBtn) {
                if (!activeBtn) return;
                indicator.style.width = activeBtn.offsetWidth + 'px';
                indicator.style.transform = 'translateX(' + activeBtn.offsetLeft + 'px)';
            }

            function refreshDayButtons(dayIndex) {
                selector.querySelectorAll('.day-selector-btn').forEach(function(btn) {
                    var isActive = Number(btn.dataset.index) === dayIndex;
                    btn.classList.toggle('active', isActive);
                    if (isActive) {
                        moveDayIndicator(btn);
                    }
                });
            }

            function buildDaySelector() {
                daysData.forEach(function(day, index) {
                    var btn = document.createElement('div');
                    btn.className = 'day-selector-btn';
                    btn.dataset.index = index;
                    btn.innerText = day.label;
                    btn.onclick = function() {
                        renderChart(index);
                    };
                    selector.appendChild(btn);
                });
                requestAnimationFrame(function() {
                    refreshDayButtons(currentDayIndex);
                });
            }

            function renderChart(dayIndex) {
                currentDayIndex = dayIndex;
                var dayInfo = daysData[dayIndex];
                var hourly_counts = dayInfo.counts;
                var max_val = Math.max(...hourly_counts);
                if (max_val === 0) max_val = 1;
                
                if (hasRenderedActivityChart) {
                    chartDom.style.opacity = '0.72';
                    chartDom.style.transform = 'translateX(14px)';
                }
                
                var data = [];
                for (var i = 0; i <= 23; i++) {
                    var count = hourly_counts[i];
                    var y = Math.sin((i - 6) / 24 * Math.PI * 2);
                    data.push([i, y, count]);
                }

                var option = {
                    backgroundColor: 'transparent',
                    grid: { top: 40, bottom: 20, left: 20, right: 20, containLabel: true },
                    xAxis: {
                        type: 'value',
                        min: 0, max: 23,
                        interval: 1,
                        axisLine: { show: false },
                        splitLine: { show: false },
                        axisTick: { show: false },
                        axisLabel: {
                            formatter: function (value) {
                                if(value === 0) return '00:00';
                                if(value === 3) return '03:00';
                                if(value === 6) return '06:00';
                                if(value === 9) return '09:00';
                                if(value === 12) return '12:00';
                                if(value === 15) return '15:00';
                                if(value === 18) return '18:00';
                                if(value === 21) return '21:00';
                                if(value === 23) return '23:59';
                                return '';
                            },
                            color: '#8b949e',
                            fontSize: 13,
                            fontFamily: 'monospace',
                            margin: 8
                        }
                    },
                    yAxis: {
                        type: 'value',
                        min: -1.2, max: 1.5,
                        show: false
                    },
                    series: [
                        {
                            type: 'line',
                            data: data.map(function (item) { return [item[0], item[1]]; }),
                            smooth: true,
                            symbol: 'none',
                            lineStyle: { color: '#30363d', width: 2 },
                            z: 2,
                            markLine: {
                                symbol: ['none', 'none'],
                                label: { show: false },
                                data: [
                                    { yAxis: 0, lineStyle: { type: 'dashed', color: '#30363d', width: 1 } }
                                ]
                            }
                        },
                        {
                            type: 'scatter',
                            data: data,
                            z: 4,
                            symbolSize: function (data) {
                                return 12 + (data[2] / max_val) * 16; 
                            },
                            itemStyle: {
                                color: function(params) {
                                    if (params.data[2] === 0) return 'rgba(88, 166, 255, 0.15)';
                                    var opacity = 0.5 + (params.data[2] / max_val) * 0.5;
                                    return 'rgba(88, 166, 255, ' + opacity + ')';
                                }
                            },
                            tooltip: {
                                formatter: function(params) {
                                    var h = params.value[0];
                                    var hStr1 = (h < 10 ? '0' + h : h) + ':00';
                                    var hStr2 = (h < 10 ? '0' + h : h) + ':59';
                                    return hStr1 + ' ~ ' + hStr2 + ' 录入/修改了 ' + params.value[2] + ' 次题目';
                                }
                            }
                        },
                        {
                            type: 'scatter',
                            data: [[6, 0, 0], [12, 1.2, 0], [18, 0, 0], [21, -0.7, 0]],
                            symbol: 'circle',
                            symbolSize: 0,
                            z: 3,
                            label: {
                                show: true,
                                formatter: function(params) {
                                    if (params.data[0] === 6) return '🌅';
                                    if (params.data[0] === 12) return '☀️';
                                    if (params.data[0] === 18) return '🌇';
                                    if (params.data[0] === 21) return '🌙';
                                    return '';
                                },
                                position: 'top',
                                distance: 14,
                                fontSize: 16
                            }
                        }
                    ],
                    tooltip: { 
                        trigger: 'item', 
                        backgroundColor: 'rgba(13, 17, 23, 0.9)', 
                        borderColor: '#30363d', 
                        textStyle: { color: '#c9d1d9' },
                        formatter: function(params) {
                            if (params.componentType === 'series' && params.seriesIndex === 1) {
                                var h = params.value[0];
                                var hStr1 = (h < 10 ? '0' + h : h) + ':00';
                                var hStr2 = (h < 10 ? '0' + h : h) + ':59';
                                return hStr1 + ' ~ ' + hStr2 + ' 录入/修改了 ' + params.value[2] + ' 次题目';
                            }
                        }
                    }
                };
                myChart.setOption(option, true);
                refreshDayButtons(dayIndex);
                requestAnimationFrame(function() {
                    chartDom.style.opacity = '1';
                    chartDom.style.transform = 'translateX(0)';
                });
                hasRenderedActivityChart = true;
            }
            
            buildDaySelector();
            renderChart(currentDayIndex);
            window.addEventListener('resize', function() {
                if (myChart) myChart.resize();
                refreshDayButtons(currentDayIndex);
            });
        }
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initChart);
        } else {
            setTimeout(initChart, 300);
        }
    </script>
    """
    return html

def generate_echarts_bar_html(data_dict, title):
    if not data_dict:
        return "<div style='color: gray;'>暂无数据</div>"
    
    sorted_items = sorted(data_dict.items(), key=lambda x: x[1], reverse=True)
    labels = [x[0] for x in sorted_items]
    values = [x[1] for x in sorted_items]
    
    labels_json = json.dumps(labels)
    values_json = json.dumps(values)
    
    html = """
    <style>
        body { margin: 0; padding: 0; background: #0d1117; }
        @keyframes chartPanelFadeUp {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .echarts-panel {
            width: 100%;
            height: 350px;
            padding: 10px 12px 6px;
            box-sizing: border-box;
            border-radius: 12px;
            border: 1px solid rgba(48, 54, 61, 0.9);
            background:
                linear-gradient(180deg, #161b22 0%, #0d1117 100%);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease;
            animation: chartPanelFadeUp 0.4s ease both;
        }
        .echarts-panel:hover {
            transform: translateY(-2px);
            border-color: rgba(88, 166, 255, 0.3);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
        }
        #bar-chart {
            width: 100%;
            height: 100%;
        }
    </style>
    <div class="echarts-panel"><div id="bar-chart"></div></div>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
    <script>
        function initChart() {
            var chartDom = document.getElementById('bar-chart');
            if (!chartDom) return;
            var myChart = echarts.init(chartDom, 'dark');
            var option = {
                backgroundColor: '#0d1117',
                tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                animationDuration: 800,
                animationEasing: 'cubicOut',
                grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
                xAxis: {
                    type: 'category',
                    data: """ + labels_json + """,
                    axisLabel: { interval: 0, rotate: 30, color: '#c9d1d9', fontWeight: 'bold' },
                    axisLine: { lineStyle: { color: '#30363d' } }
                },
                yAxis: {
                    type: 'value',
                    splitLine: { lineStyle: { color: '#30363d', type: 'dashed' } },
                    axisLabel: { color: '#c9d1d9', fontWeight: 'bold' }
                },
                series: [{
                    data: """ + values_json + """,
                    type: 'bar',
                    barWidth: '40%',
                    itemStyle: {
                        borderRadius: [6, 6, 0, 0],
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#58a6ff' },
                            { offset: 1, color: '#1f6feb' }]
                        )
                    }
                }]
            };
            myChart.setOption(option);
            window.addEventListener('resize', function() { myChart.resize(); });
        }
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initChart);
        } else {
            setTimeout(initChart, 300);
        }
    </script>
    """
    return html

def generate_echarts_pie_html(data_dict, diff_dict, title):
    if not data_dict and not diff_dict:
        return "<div style='color: gray;'>暂无数据</div>"
    
    pie_data_inner = []
    for k, v in data_dict.items():
        if isinstance(k, dict): k = str(k)
        pie_data_inner.append({"name": k, "value": v})
    
    pie_data_outer = []
    for k, v in diff_dict.items():
        if isinstance(k, dict): k = str(k)
        pie_data_outer.append({"name": k, "value": v})
    
    inner_names = [item['name'] for item in pie_data_inner]
    outer_names = [item['name'] for item in pie_data_outer]
    
    inner_names_json = json.dumps(inner_names)
    outer_names_json = json.dumps(outer_names)
    pie_data_inner_json = json.dumps(pie_data_inner)
    pie_data_outer_json = json.dumps(pie_data_outer)
    
    html = """
    <style>
        body { margin: 0; padding: 0; background: #0d1117; }
        @keyframes piePanelFadeUp {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .pie-panel {
            width: 100%;
            height: 350px;
            padding: 10px 12px 6px;
            box-sizing: border-box;
            border-radius: 12px;
            border: 1px solid rgba(48, 54, 61, 0.9);
            background:
                linear-gradient(180deg, #161b22 0%, #0d1117 100%);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease;
            animation: piePanelFadeUp 0.4s ease both;
        }
        .pie-panel:hover {
            transform: translateY(-2px);
            border-color: rgba(88, 166, 255, 0.3);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
        }
        #pie-chart {
            width: 100%;
            height: 100%;
        }
    </style>
    <div class="pie-panel"><div id="pie-chart"></div></div>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
    <script>
        function initChart() {
            var chartDom = document.getElementById('pie-chart');
            if (!chartDom) return;
            var myChart = echarts.init(chartDom, 'dark');
            var option = {
                backgroundColor: '#0d1117',
                animationDuration: 850,
                animationEasing: 'cubicOut',
                tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c} ({d}%)' },
                legend: [
                    { top: '5%', right: '5%', textStyle: { color: '#8b949e', fontSize: 12 }, orient: 'vertical', data: """ + inner_names_json + """ },
                    { top: '25%', right: '5%', textStyle: { color: '#8b949e', fontSize: 12 }, orient: 'vertical', data: """ + outer_names_json + """ }
                ],
                color: ['#58a6ff', '#3fb950', '#d29922', '#db6d28', '#f0883e', '#39c5cf', '#8957e5', '#10b981', '#58a6ff'],
                series: [
                    {
                        name: '题型分布',
                        type: 'pie',
                        selectedMode: 'single',
                        radius: [0, '35%'],
                        center: ['50%', '55%'],
                        label: { position: 'inner', fontSize: 12, fontWeight: 'bold', color: '#c9d1d9' },
                        labelLine: { show: false },
                        data: """ + pie_data_inner_json + """
                    },
                    {
                        name: '难度分布',
                        type: 'pie',
                        radius: ['50%', '70%'],
                        center: ['50%', '55%'],
                        label: { fontSize: 11, color: '#c9d1d9', position: 'outside' },
                        labelLine: { lineStyle: { color: '#30363d' }, length: 10, length2: 10 },
                        data: """ + pie_data_outer_json + """
                    }
                ]
            };
            myChart.setOption(option);
            window.addEventListener('resize', function() { myChart.resize(); });
        }
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initChart);
        } else {
            setTimeout(initChart, 300);
        }
    </script>
    """
    return html
