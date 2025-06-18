
import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Treatment Cost Optimizer", layout="wide")

# App title
st.title("Treatment Cost Optimizer")
st.markdown("Optimize healthcare spending by comparing provider costs and ratings.")

# Sidebar with filters and branding
st.sidebar.image("https://via.placeholder.com/150x50.png?text=Your+Logo", use_container_width=True)
st.sidebar.header("Filter Options")

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type="csv")

# Load dataset
def get_default_data():
    return pd.DataFrame({
        'Provider': ['Hospital A', 'Hospital B', 'Clinic C', 'Hospital D'],
        'Treatment': ['MRI Scan', 'MRI Scan', 'MRI Scan', 'MRI Scan'],
        'Cost': [1200, 950, 700, 1100],
        'Insurance Plan': ['Plan X', 'Plan Y', 'Plan X', 'Plan Y'],
        'Insurance Discount': [0.1, 0.15, 0.05, 0.2],
        'Hospital Rating': [4.5, 4.2, 3.8, 4.7]
    })

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
    except Exception as e:
        st.error(f"Error loading file: {e}")
        df = get_default_data()
else:
    df = get_default_data()

# Show preview of uploaded/default data
with st.expander("Preview Dataset"):
    st.dataframe(df)

# Dropdowns for filtering
treatment_options = df['Treatment'].unique()
insurance_options = df['Insurance Plan'].unique()

treatment = st.sidebar.selectbox("Select Treatment", treatment_options)
insurance_plan = st.sidebar.selectbox("Select Insurance Plan", insurance_options)

# Optimization logic
def find_best_treatment_option(df, treatment, insurance_plan):
    options = df[(df['Treatment'] == treatment) & (df['Insurance Plan'] == insurance_plan)].copy()

    if options.empty:
        return None

    options['Final Cost'] = options['Cost'] * (1 - options['Insurance Discount'])
    options['Score'] = options['Final Cost'] / options['Hospital Rating']
    best_option = options.loc[options['Score'].idxmin()]

    return {
        'Best Provider': best_option['Provider'],
        'Original Cost': best_option['Cost'],
        'Final Cost (After Insurance)': best_option['Final Cost'],
        'Hospital Rating': best_option['Hospital Rating']
    }

# Run optimizer
st.subheader("Optimization Result")
if st.button("Find Best Option"):
    result = find_best_treatment_option(df, treatment, insurance_plan)
    if result:
        st.success(f"**Best Provider: {result['Best Provider']}**")
        st.write(f"**Original Cost:** ${result['Original Cost']:.2f}")
        st.write(f"**Final Cost (After Insurance):** ${result['Final Cost (After Insurance)']:.2f}")
        st.write(f"**Hospital Rating:** {result['Hospital Rating']}/5")

        export_data = pd.DataFrame([result])

        # Download CSV
        csv = export_data.to_csv(index=False).encode('utf-8')
        st.download_button("Download Result as CSV", csv, "result.csv", "text/csv")
    else:
        st.error("No data available for the selected treatment and insurance plan.")
