import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

st.title('Recurring vs Active vs Regular Customer')
st.sidebar.markdown("## Page 1")
def load_Regularity_data():
    data = pd.read_excel('All_columns_new.xlsx')
    return data

def load_active_data():
    data = pd.read_excel('All_columns.xlsx')
    return data

Regularity=load_Regularity_data()
active = load_active_data()

locations = active.salesperson.unique().tolist()
options = st.sidebar.multiselect('select salesperson name',locations)


locations1 = active.TL_PORT_PAIR.unique().tolist()
options1 = st.sidebar.multiselect('select  TL_PORT_PAIR  name',locations1)
#st.write('You have selected:', options)

#st.markdown("# Page 1")
#st.sidebar.markdown("## Page 1")

Regularity = Regularity[Regularity['salesperson'].isin(options)]
a = Regularity.groupby(['salesperson','Customer Purchase Pattern']).size().unstack()
b = Regularity.groupby(['salesperson','Customer Purchase Pattern']).size().unstack().apply(lambda x: x/a.sum(axis =1)*100)
ax = b.plot.bar(stacked = True)
for rect in ax.patches:
    height = rect.get_height()
    width = rect.get_width()
    x = rect.get_x()
    y = rect.get_y()

    total = len(Regularity['salesperson'])
    
    label_text = '{:.1f}%'.format(height)
    label_x = x + width / 2
    label_y = y + height / 2
    ax.text(label_x, label_y, label_text, ha='center', va='center', fontsize=10)
    plt.xticks(rotation=0)
    plt.title('One-Time vs Recurring Customer')
    plt.xlabel('Salesperson')
    st.set_option('deprecation.showPyplotGlobalUse', False)
plt.show()
st.pyplot()

active = active[active['salesperson'].isin(options)]
active['Inactive Customer Indicator'] = np.where(active['Inactive Customer Indicator'] == True, 'Inactive', 'Active')
active['Regularity'] = np.where(active['Regularity'] == 1, 'Regular', 'Irregular')

import matplotlib.pyplot as plt
a = active.groupby(['salesperson','Inactive Customer Indicator']).size().unstack()
b = active.groupby(['salesperson','Inactive Customer Indicator']).size().unstack().apply(lambda x: x/a.sum(axis =1)*100)
ax = b.plot.bar(stacked = True)
for rect in ax.patches:
    height = rect.get_height()
    width = rect.get_width()
    x = rect.get_x()
    y = rect.get_y()

    total = len(active['salesperson'])
    
    label_text = '{:.1f}%'.format(height)
    label_x = x + width / 2
    label_y = y + height / 2
    ax.text(label_x, label_y, label_text, ha='center', va='center', fontsize=10)
    plt.xticks(rotation=0)
    plt.title('Active vs Inactive')
    plt.xlabel('Salesperson')
plt.show()
st.pyplot()
#st.altair_chart(ax1 | ax2)


import matplotlib.pyplot as plt
a = active.groupby(['salesperson','Regularity']).size().unstack()
b = active.groupby(['salesperson','Regularity']).size().unstack().apply(lambda x: x/a.sum(axis =1)*100)
ax = b.plot.bar(stacked = True)
for rect in ax.patches:
    height = rect.get_height()
    width = rect.get_width()
    x = rect.get_x()
    y = rect.get_y()

    total = len(active['salesperson'])
    
    label_text = '{:.1f}%'.format(height)
    label_x = x + width / 2
    label_y = y + height / 2
    ax.text(label_x, label_y, label_text, ha='center', va='center', fontsize=10)
    plt.xticks(rotation=0)
    plt.title('Regular vs Irregular')
    plt.xlabel('Salesperson')
plt.show()
st.pyplot()

import matplotlib.pyplot as plt
active = active[active['salesperson'].isin(options)]
df=active.groupby(['TL_PORT_PAIR','salesperson']).agg({'Frequency':'count'}).reset_index()
diff=active.groupby(['TL_PORT_PAIR','salesperson']).agg({'Profit/CBM':sum}).reset_index().rename({'Profit/CBM':'GrossProfit_per_CBM'},axis=1)
diff['GrossProfit_per_CBM']=round(diff['GrossProfit_per_CBM'],1)
color_discrete_sequence = ['orange','#7CFC00']
fig = px.bar(diff, x="TL_PORT_PAIR", y="GrossProfit_per_CBM", color="salesperson", text_auto=True,
              title="Tradelane Vs. salerep w.r.t. Grossprofit per CBM",color_discrete_sequence=color_discrete_sequence)
fig.update_layout(height=600,width=900)
st.plotly_chart(fig)

color_discrete_sequence = ['orange','#7CFC00']
fig = px.bar(df, x="TL_PORT_PAIR", y="Frequency", color="salesperson", text_auto=True,
             title="Tradelane Vs. salerep w.r.t. Frequency",
            color_discrete_sequence=color_discrete_sequence)
fig.update_layout(height=700,width=900)
st.plotly_chart(fig)

from pathlib import Path
with Path("Tradelane Vs. salerep w.r.t. Grossprofit per CBM.html").open("w") as f:
    f.write(fig.to_html())