import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st


from src.DataAnalysis.data_analysis import (
    load_data,
    cross_tabulation,
    chi_square_test,
    most_common_varieties,
    yield_analysis,
    plot_yield_analysis,
    plot_variety_by_origin,
    plot_correlation_heatmap,
)
from src.ModelTraining.model_interface import (
    load_model,
    generate_dropdown_options,
    make_prediction,
    display_metrics,
)


model_path = "src/ModelTraining/random_forest_model.pkl"
encoders_path = "src/ModelTraining/label_encoders.pkl"
metrics_path = "src/ModelTraining/metrics.tsv"
model, label_encoders = load_model(model_path, encoders_path)

# Load data
st.title("Coffee Data Analysis Dashboard")
data_filepath = "data/03_final/merged_files.tsv"

st.sidebar.header("Analysis Options")
analysis_type = st.sidebar.selectbox(
    "Choose an analysis type",
    [
        "Overview",
        "Cross-tabulation",
        "Most Common Varieties",
        "Yield Potential Analysis",
        "Variety by Origin",
        "Correlation Heatmap",
        "Model",
        "Model metrics",
    ],
)

# Load the dataset
data = load_data(data_filepath)

if analysis_type == "Overview":
    st.header("Dataset Overview")
    st.write(data.head())
    st.write("The table above showcases the structure of the dataset.")
    st.markdown("### Summary Statistics:")
    st.write(data.describe(include="all"))
    st.write("Those statistics provide a summary of the data.")
    st.markdown("### Summary:")
    st.markdown(
        "1. Brasil, Ethiopia and Kenya are the dominant origins.\n"
        "2. Cattura and catuai are the dominant varieties.\n"
        "3. Cross-tabulation indicates a strong relationship between varietal and other variables. It's an important"
        "factor for model creation since it's the variety that we wish to predict.\n"
        "4. Chi2 values are high across different variables suggesting a significant relationship between the variables.\n"
        "5. Besides that not all of the above received a very low p2 score which means not all of the relations are "
        "statistically significant at any reasonable confidence level. All relations however received a p score of 0 "
        "when it came to variety. It's a key factor for prediction since we have multiple variables that can be provided"
        "for the model to predict the best suited varietal.\n"
        "6. In `Yield Potential Analysis by Variety` we can see that varieties with high or medium yields are the most"
        "common in the dataset. It makes sense since they yield the most coffee meaning they are sold in higher quantities.\n"
        "7. Due to the difficulty of fact-checking Etihopian varities, all of Ethopian beans have been labeled as "
        "Heirloom which is further discussed in Model overview.\n"
        "8. When choosing our approach to the model it's crucial to use something that has a robust approach to overfitting."
    )

elif analysis_type == "Cross-tabulation":
    st.header("Cross-tabulation Analysis")
    st.write(
        "Upon selecting 2 columns from the dataset, a table will be displayed. It shows the relationship between the two columns as well as Chi-square test which statistically validates whether the observed relationships are significant or due to random chance."
    )
    st.write(
        "High chi2 value will showcase a strong deviation from the assumption of independence, suggesting a significant relationship between the variables being tested."
    )
    st.write(
        "p_value of 0 indicates that the observed relationship is statistically significant at any reasonable confidence level."
    )
    col1 = st.selectbox("Choose Column 1", data.columns)
    col2 = st.selectbox("Choose Column 2", data.columns)

    if col1 != col2:
        cross_tab = cross_tabulation(data, col1, col2)
        st.write("Cross-tabulation Table:")
        st.write(cross_tab)

        chi2_results = chi_square_test(cross_tab)
        st.write("Chi-Square Test Results:")
        st.json(chi2_results)

elif analysis_type == "Most Common Varieties":
    st.header("Most Common Varieties by Origin")
    common_varieties = most_common_varieties(data)
    st.write(common_varieties)

elif analysis_type == "Yield Potential Analysis":
    st.header("Yield Potential Analysis by Variety")
    yield_data = yield_analysis(data)
    st.write(yield_data)

    st.pyplot(plot_yield_analysis(yield_data))

elif analysis_type == "Variety by Origin":
    st.header("Varieties by Origin")
    st.pyplot(plot_variety_by_origin(data))

elif analysis_type == "Correlation Heatmap":
    st.header("Correlation Heatmap")
    st.write(
        "Please use streamlit's build in full screen functionality to interpret this heatmap.."
    )
    st.pyplot(plot_correlation_heatmap(data))

elif analysis_type == "Model":
    st.header("Predict Coffee Variety")

    # Generate dropdown options
    dropdowns = generate_dropdown_options(
        label_encoders,
        [
            "origin",
            "Yield Potential",
            "Quality potential at high altitude",
            "Optimal Altitude",
            "Coffee leaf rust",
            "Nematode",
            "Coffee Berry Disease",
        ],
    )

    # User input form
    user_input = {}
    for feature, options in dropdowns.items():
        user_input[feature] = st.selectbox(f"Select {feature}", options)

    # Predict button
    if st.button("Predict"):
        prediction = make_prediction(model, label_encoders, user_input)
        st.subheader("Prediction")
        st.write(f"The predicted coffee variety is: **{prediction}**")

elif analysis_type == "Model metrics":
    st.header("Model metrics & overview")
    st.markdown("### Why Random Forest?")
    st.markdown(
        "1. Our task is a prediction of coffee variety.\n"
        "2. In this dataset both categorical and numerical data are present. Both are handled seamlessly"
        "in a random forest.\n"
        "3. With a limited sample random forest is great due to its robustness to overfitting. For example here we have "
        "a big dominant of Brazilian coffee.\n"
    )
    metrics = display_metrics(metrics_path)
    st.write("Performance Metrics:")
    st.dataframe(metrics)
    st.markdown("### Metrics overview")
    st.markdown(
        "1. We have a high accuracy meaning the percentage of correct predictions is high.\n"
        "2. Due to lack of robust data about Heirloom varieties and the common labeling of Ethiopian beans as just "
        "heirloom, in this dataset we see a direct correlation of Heirloom to Ethiopian coffee. "
        "This is also largely true in real life as Ethiopia is the birthplace of coffee. Farming in this country is "
        "mostly done by gathering wildly grown beans which means it's extremely hard to label beans.\n"
        "3. Macro Average Precision and Recall show that the model is right in most cases.\n"
        "4. High F1-scores indicate that the model is good at both correctly identifying samples (recall) and making "
        "correct predictions (precision) across all coffee varieties.\n"
        "5. With all of the above we can say that the model is performing well and seems consistent across classes.\n"
        "6. The weighted averages show that the model balances predictions for both frequent and infrequent coffee "
        "varieties effectively.\n"
    )
