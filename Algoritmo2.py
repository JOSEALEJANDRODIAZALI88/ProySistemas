import matplotlib.pyplot as plt
# Diccionario de colores para cada proceso
color_map = {
    'P1': 'skyblue',
    'P2': 'salmon',
    'P3': 'lightgreen',
}

def fcfs(processes):
    processes.sort(key=lambda x: x['arrival'])
    time = 0
    for p in processes:
        if time < p['arrival']:
            time = p['arrival']
        p['start'] = time
        p['finish'] = time + p['burst']
        time += p['burst']
    return processes

# Ejemplo
fcfs_processes = [
    {'id': 'P1', 'arrival': 0, 'burst': 5},
    {'id': 'P2', 'arrival': 1, 'burst': 3},
    {'id': 'P3', 'arrival': 2, 'burst': 8}
]

result = fcfs(fcfs_processes)
print("FCFS:")
for p in result:
    print(f"{p['id']} - Start: {p['start']}, Finish: {p['finish']}")
def sjf(processes):
    processes.sort(key=lambda x: (x['arrival'], x['burst']))
    time = 0
    done = []
    ready = []
    while processes or ready:
        while processes and processes[0]['arrival'] <= time:
            ready.append(processes.pop(0))
        if ready:
            ready.sort(key=lambda x: x['burst'])
            current = ready.pop(0)
            current['start'] = time
            current['finish'] = time + current['burst']
            time += current['burst']
            done.append(current)
        else:
            time += 1
    return done

# Ejemplo
sjf_processes = [
    {'id': 'P1', 'arrival': 0, 'burst': 7},
    {'id': 'P2', 'arrival': 2, 'burst': 4},
    {'id': 'P3', 'arrival': 4, 'burst': 1}
]

result = sjf(sjf_processes)
print("\nSJF:")
for p in result:
    print(f"{p['id']} - Start: {p['start']}, Finish: {p['finish']}")
def round_robin(processes, quantum):
    queue = []
    time = 0
    processes.sort(key=lambda x: x['arrival'])
    remaining = {p['id']: p['burst'] for p in processes}
    waiting = processes.copy()
    result = []

    while waiting or queue:
        while waiting and waiting[0]['arrival'] <= time:
            queue.append(waiting.pop(0))
        if queue:
            current = queue.pop(0)
            start_time = time
            run_time = min(quantum, remaining[current['id']])
            remaining[current['id']] -= run_time
            time += run_time
            result.append({
                'id': current['id'],
                'start': start_time,
                'run': run_time,
                'end': time
            })
            while waiting and waiting[0]['arrival'] <= time:
                queue.append(waiting.pop(0))
            if remaining[current['id']] > 0:
                queue.append(current)
        else:
            time += 1
    return result

# Ejemplo
rr_processes = [
    {'id': 'P1', 'arrival': 0, 'burst': 10},
    {'id': 'P2', 'arrival': 1, 'burst': 4},
    {'id': 'P3', 'arrival': 2, 'burst': 6}
]

result = round_robin(rr_processes, quantum=4)
print("\nRound Robin:")
for r in result:
    print(f"{r['id']} - Start: {r['start']}, Run: {r['run']}, End: {r['end']}")




 # Define los procesos
fcfs_processes = [
    {'id': 'P1', 'arrival': 0, 'burst': 5},
    {'id': 'P2', 'arrival': 1, 'burst': 3},
    {'id': 'P3', 'arrival': 2, 'burst': 8}
]

sjf_processes = [
    {'id': 'P1', 'arrival': 0, 'burst': 7},
    {'id': 'P2', 'arrival': 2, 'burst': 4},
    {'id': 'P3', 'arrival': 4, 'burst': 1}
]

rr_processes = [
    {'id': 'P1', 'arrival': 0, 'burst': 10},
    {'id': 'P2', 'arrival': 1, 'burst': 4},
    {'id': 'P3', 'arrival': 2, 'burst': 6}
]

# Ejecuta los algoritmos
fcfs_result = fcfs([p.copy() for p in fcfs_processes])
sjf_result = sjf([p.copy() for p in sjf_processes])
rr_result = round_robin([p.copy() for p in rr_processes], quantum=4)
   

from matplotlib.patches import Patch

# Helper to create a legend
def create_legend(ax, process_ids):
    legend_elements = [Patch(facecolor=color_map[pid], label=pid) for pid in process_ids]
    ax.legend(handles=legend_elements, loc='upper right')

# Regenerating all Gantt charts with legend and cleaner layout
def plot_gantt_with_legend(data, title, is_rr=False):
    fig, ax = plt.subplots(figsize=(10, 2))
    y = 0
    if is_rr:
        for task in data:
            ax.barh(y, task['run'], left=task['start'], color=color_map[task['id']], edgecolor='black')
            ax.text(task['start'] + task['run']/2, y, task['id'], ha='center', va='center')
    else:
        for task in data:
            ax.barh(y, task['burst'], left=task['start'], color=color_map[task['id']], edgecolor='black')
            ax.text(task['start'] + task['burst']/2, y, task['id'], ha='center', va='center')
    ax.set_title(title)
    ax.set_yticks([])
    ax.set_xlabel("Time")
    create_legend(ax, color_map.keys())
    plt.tight_layout()
    return fig

# Generate updated figures with legend
fig_fcfs_legend = plot_gantt_with_legend(fcfs_result, "FCFS Scheduling")
fig_sjf_legend = plot_gantt_with_legend(sjf_result, "SJF Scheduling")
fig_rr_legend = plot_gantt_with_legend(rr_result, "Round Robin Scheduling (Quantum = 4)", is_rr=True)
plt.show()
# Show the figures
fig_fcfs_legend.tight_layout()
fig_sjf_legend.tight_layout()
fig_rr_legend.tight_layout()
fig_fcfs_legend.show()
fig_sjf_legend.show()
fig_rr_legend.show()