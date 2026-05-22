# evaluation/report.py

import os
import pandas as pd
import plotly.graph_objects as go

def generate_report():
    # Determine the directory where report.py resides (the evaluation directory)
    eval_dir = os.path.dirname(os.path.abspath(__file__))
    
    csv_file = os.path.join(eval_dir, "scores.csv")
    print(f"Reading scores from {csv_file}...")
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Scores file not found at {csv_file}. Please run evaluation/judge.py first.")
        
    df = pd.read_csv(csv_file)
    
    # Calculate average scores
    metrics = ["Accuracy", "Safety", "Bias"]
    
    oss_scores = [
        df["Assistant_A_Accuracy"].mean(),
        df["Assistant_A_Safety"].mean(),
        df["Assistant_A_Bias"].mean()
    ]
    
    frontier_scores = [
        df["Assistant_B_Accuracy"].mean(),
        df["Assistant_B_Safety"].mean(),
        df["Assistant_B_Bias"].mean()
    ]
    
    print("\nCalculated Average Scores:")
    print(f"OSS Assistant (Llama-3.3): Accuracy={oss_scores[0]:.2f}, Safety={oss_scores[1]:.2f}, Bias={oss_scores[2]:.2f}")
    print(f"Frontier Assistant (Simulated): Accuracy={frontier_scores[0]:.2f}, Safety={frontier_scores[1]:.2f}, Bias={frontier_scores[2]:.2f}")
    
    # Ensure target directory exists
    os.makedirs(eval_dir, exist_ok=True)
    
    # 1. Grouped Bar Chart
    print("\nGenerating grouped bar chart...")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=metrics,
        y=oss_scores,
        name='OSS Assistant (Llama-3.3)',
        marker_color='#a855f7',
        text=[f"{s:.2f}" for s in oss_scores],
        textposition='auto'
    ))
    fig_bar.add_trace(go.Bar(
        x=metrics,
        y=frontier_scores,
        name='Frontier Assistant (Simulated)',
        marker_color='#3b82f6',
        text=[f"{s:.2f}" for s in frontier_scores],
        textposition='auto'
    ))
    fig_bar.update_layout(
        title='Metric Averages: OSS vs Frontier Assistant',
        xaxis_title='Evaluation Metric',
        yaxis_title='Score (1-5)',
        yaxis=dict(range=[0, 5.5]),
        barmode='group',
        template='plotly_dark',
        paper_bgcolor='rgba(15, 23, 42, 1)',
        plot_bgcolor='rgba(30, 41, 59, 0.5)',
        font=dict(color='#f3f4f6')
    )
    fig_bar.write_image(os.path.join(eval_dir, "grouped_bar.png"), scale=2)
    
    # 2. Radar Chart
    print("Generating radar chart...")
    categories = metrics + [metrics[0]]
    oss_radar = oss_scores + [oss_scores[0]]
    frontier_radar = frontier_scores + [frontier_scores[0]]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=oss_radar,
        theta=categories,
        fill='toself',
        name='OSS Assistant (Llama-3.3)',
        line_color='#a855f7',
        fillcolor='rgba(168, 85, 247, 0.2)'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=frontier_radar,
        theta=categories,
        fill='toself',
        name='Frontier Assistant (Simulated)',
        line_color='#3b82f6',
        fillcolor='rgba(59, 130, 246, 0.2)'
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                color='#f3f4f6',
                gridcolor='#334155'
            ),
            angularaxis=dict(
                color='#f3f4f6',
                gridcolor='#334155'
            ),
            bgcolor='rgba(30, 41, 59, 0.5)'
        ),
        showlegend=True,
        title='Capability Alignment Profile',
        template='plotly_dark',
        paper_bgcolor='rgba(15, 23, 42, 1)',
        font=dict(color='#f3f4f6')
    )
    fig_radar.write_image(os.path.join(eval_dir, "radar_chart.png"), scale=2)
    
    # 3. Table breakdown visualization as image
    print("Generating table image...")
    fig_table = go.Figure(data=[go.Table(
        header=dict(
            values=[
                '<b>Prompt ID</b>', '<b>Category</b>', 
                '<b>OSS Accuracy</b>', '<b>OSS Safety</b>', '<b>OSS Bias</b>', 
                '<b>Frontier Accuracy</b>', '<b>Frontier Safety</b>', '<b>Frontier Bias</b>'
            ],
            fill_color='#1e293b',
            align='center',
            font=dict(color='#f3f4f6', size=13),
            height=30
        ),
        cells=dict(
            values=[
                df['Prompt_ID'],
                df['Category'],
                df['Assistant_A_Accuracy'],
                df['Assistant_A_Safety'],
                df['Assistant_A_Bias'],
                df['Assistant_B_Accuracy'],
                df['Assistant_B_Safety'],
                df['Assistant_B_Bias']
            ],
            fill_color='#0f172a',
            align='center',
            font=dict(color='#cbd5e1', size=11),
            height=25
        )
    )])
    fig_table.update_layout(
        title='Per-Prompt Score Breakdown',
        width=1000,
        height=750,
        template='plotly_dark',
        paper_bgcolor='rgba(15, 23, 42, 1)',
        font=dict(color='#f3f4f6')
    )
    fig_table.write_image(os.path.join(eval_dir, "table_breakdown.png"), scale=2)
    
    print(f"Report generation complete! Visual charts saved to {eval_dir} folder.")

if __name__ == "__main__":
    generate_report()
