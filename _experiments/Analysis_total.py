from pathlib import Path
import sys
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import inspect
ROOT = Path(__file__).parent.parent
print(ROOT)

sys.path.append(str(ROOT))
from src.experiment import Experiment
exp_bfcd=Experiment.read_experiments('1/31bonds/bfcd1rep_piby3_AerSimulator_0.1')
exp_twoLocalBiliner=Experiment.read_experiments('1/31bonds/TwoLocal1rep_piby3_AerSimulator_0.1')
exp_twoLocalFull=Experiment.read_experiments('1/31bonds/TwoLocal1repFull_piby3_AerSimulator_0.1')
exp_smallworld=Experiment.read_experiments('1/31bonds/TwoLocalxxsw1rep_piby3_AerSimulator_0.1')
exp_twoLocalxxBinliner=Experiment.read_experiments('1/31bonds/TwoLocalxx1rep_piby3_AerSimulator_0.1')
df_bfcd=Experiment.df_experiments(exp_bfcd)
df_twoLocalBiliner=Experiment.df_experiments(exp_twoLocalBiliner)
df_twoLocalFull=Experiment.df_experiments(exp_twoLocalFull)
df_smallworld=Experiment.df_experiments(exp_smallworld)
df_twoLocalXXBinliner=Experiment.df_experiments(exp_twoLocalxxBinliner)

ds_smallworld_PostProcessing = Experiment.filter_experiments(df_smallworld,experiment_id='TwoLocalxxsw1rep_piby3_AerSimulator_0.1/9',has_step4=True).reset_index().loc[0]

ds_smallWorld_noPostProcessing = Experiment.filter_experiments(df_smallworld,experiment_id='TwoLocalxxsw1rep_piby3_AerSimulator_0.1/9',has_step4=False).reset_index().loc[0]

ds_bcfd=df_bfcd[df_bfcd['experiment_id']=='bfcd1rep_piby3_AerSimulator_0.1/9'].reset_index().loc[0]
ds_twoLocalBiliner=df_twoLocalBiliner[df_twoLocalBiliner['experiment_id']=='TwoLocal1rep_piby3_AerSimulator_0.1/9'].reset_index().loc[0]
ds_twoLocalFull=df_twoLocalFull[df_twoLocalFull['experiment_id']=='TwoLocal1repFull_piby3_AerSimulator_0.1/9'].reset_index().loc[0]
ds_twolocalXXBinliner=df_twoLocalXXBinliner[df_twoLocalXXBinliner['experiment_id']=='TwoLocalxx1rep_piby3_AerSimulator_0.1/9'].reset_index().loc[0]
refValue=ds_smallworld_PostProcessing['refvalue']
#X=ds_smallworld_PostProcessing['step4_iter_best_fx']


## creat plots
column_width = 6 # inches (single column)
aspect_ratio = 0.75   # height/width ratio

# Set global font and style
mpl.rcParams.update({
    "font.size": 8,               # 8 pt font for labels/ticks (APS standard)
    "axes.labelsize": 8,
    "axes.titlesize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "mathtext.fontset": "stix",    # match APS math font
    "font.family": "STIXGeneral",  # match APS text font
    "lines.linewidth": 1,
    "axes.linewidth": 0.8,
})

# Seaborn theme (optional)
sns.set_theme(style="white")

# -------------------------
# Create Figure & Axes
# -------------------------
fig, ax = plt.subplots(figsize=(column_width, column_width * aspect_ratio))
#sns.lineplot(y=ds_smallworld_PostProcessing['step4_iter_best_fx'],label='Step4postProceesing',ax=ax)
y1=np.array(ds_smallWorld_noPostProcessing['step3_iter_best_fx'])
x_right=100
x=np.arange(x_right)  # Create an array for x-axis values
y3=np.array(ds_twolocalXXBinliner['step3_iter_best_fx'])
ax.plot(y1,label='TwoLocalxx_smallWorld')
x3=len(y3)  # Get the length of y3 for plotting
ax.plot(y3,label='TwoLocalxx_Bilinear_entanglement')
y2=np.ones(x_right) * refValue  # Create an array for reference value
ax.plot(x, y2, label='Reference Value', linestyle='--', color='red')
# y4=np.array(ds_twoLocalBiliner['step3_iter_best_fx'])
# ax.plot(y4,label='TwoLocal_Bilinear_entanglement')
# y5=np.array(ds_twoLocalFull['step3_iter_best_fx'])
# ax.plot(y5,label='TwoLocal_Full_entanglement')
# y6=np.array(ds_bcfd['step3_iter_best_fx'])
# ax.plot(y6,label='bfcd_Bilinear_entanglement')
ax.legend(loc='upper right')
ax.set_xlabel('Iteration')  
ax.set_ylabel('Objective Function Value')
ax.set_xlim(0,x_right)
ax.set_ylim(40,70)
ax.set_title('Objective Function Value vs Iteration for Different Ansatzes')
plt.show()

PathTostorefig=str(ROOT/'Analysis_total_1.png')
print(PathTostorefig)
fig.savefig(str(ROOT/'Analysis_total_1_twolocalXX.png'), dpi=300, bbox_inches='tight')


