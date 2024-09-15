from bs4 import BeautifulSoup
import pandas as pd
import os


# Parse the HTML file
def parse_html(html_file):
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Extract the relevant table rows
    table_rows = soup.find("table", class_="index").find("tbody").find_all("tr")

    data = []

    for row in table_rows:
        cells = row.find_all("td")

        file_reference = cells[0].find("a")["href"].strip()
        file_path = cells[0].text.strip()

        if "__init__.py" in file_path or "version.py" in file_path:
            continue

        statements = int(cells[1].text.strip())
        missing = int(cells[2].text.strip())
        coverage = float(cells[4].text.strip().replace("%", ""))

        # Split path to container and module
        path_parts = file_path.split("/")
        container = path_parts[0]

        module = "/".join(path_parts[1:]) if len(path_parts) > 1 else ""
        other_file_path = ""

        if container == "nvidia_tao_pytorch":
            if path_parts[1] == "api":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "core":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "cv":
                module = path_parts[1] + "/" + path_parts[2]
                other_file_path = (
                    "/".join(path_parts[3:]) if len(path_parts) > 3 else ""
                )
            if path_parts[1] == "pointcloud":
                module = path_parts[1] + "/" + path_parts[2]
                other_file_path = (
                    "/".join(path_parts[3:]) if len(path_parts) > 3 else ""
                )
            if path_parts[1] == "pruning":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "config":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            

        elif container == "nvidia_tao_deploy":
            if path_parts[1] == "api":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "cv":
                module = path_parts[1] + "/" + path_parts[2]
                other_file_path = (
                    "/".join(path_parts[3:]) if len(path_parts) > 3 else ""
                )
            if path_parts[1] == "dataloader":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "engine":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "inferencer":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "metrics":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "utils":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "config":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])

        elif container == "nvidia_tao_ds":
            if path_parts[1] == "api":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "annotations":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "augment":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "auto_label":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "backbone":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "config_utils":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "core":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "data_analytics":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "image":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "json_schema_converter":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "dataclass_to_rst":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])

        else:
            # nvidia_tao_tf2
            if path_parts[1] == "api":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "backbones":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "blocks":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "common":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "config_utils":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "cv":
                module = path_parts[1] + "/" + path_parts[2]
                other_file_path = (
                    "/".join(path_parts[3:]) if len(path_parts) > 3 else ""
                )
            if path_parts[1] == "experimental":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            if path_parts[1] == "model_optimization":
                module = path_parts[1]
                other_file_path = "/".join(path_parts[2:])
            
        data.append(
            {
                "container": container,
                "module": module,
                "other_file_path": other_file_path,
                "file_reference": file_reference,
                "statements": statements,
                "missing": missing,
                "coverage": coverage,
            }
        )

    return pd.DataFrame(data)


# Create a new HTML report
def create_html_report_per_container_and_module(df_table, output_dir):

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    html_content = """
    <html>
    <head>
        <title>Code Coverage Report per Container and Module</title>
    </head>
    <body>
        <h1>Code Coverage Report per Container and Module</h1>
        <table border="1">
            <thead>
                <tr>
                    <th>Container</th>
                    <th>Module</th>
                    <th>File Path</th>
                    <th>Total Statements</th>
                    <th>Total Missing</th>
                    <th>Coverage</th>
                </tr>
            </thead>
            <tbody>
    """

    file_name = (
        f"{df_table['container'][0]}_{df_table['module'][0].replace('/', '_')}.html"
    )
    file_path = os.path.join(output_dir, file_name)

    # Add rows to the table
    for _, row in df_table.iterrows():
        html_content += f"""
        <tr>
            <td>{row['container']}</td>
            <td><a href="../../htmlcov/{row['file_reference']}">{row['module']}</a></td>
            <td><a href="../../htmlcov//{row['file_reference']}">{row['other_file_path']}</a></td>
            <td>{row['total_statements']}</td>
            <td>{row['total_missing']}</td>
            <td>{row['total_coverage']:.2f}%</td>
        </tr>
        """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)


def create_all_modules_per_container_html_report(low_coverage_modules, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    html_content = """
    <html>
    <head>
        <title>Code Coverage Report per Container</title>
    </head>
    <body>
        <h1>Code Coverage Report per Container</h1>
        <table border="1">
            <thead>
                <tr>
                    <th>Container</th>
                    <th>Module</th>
                    <th>File Path</th>
                    <th>Coverage</th>
                </tr>
            </thead>
            <tbody>
    """
    file_name = low_coverage_modules["container"].iloc[0] + "_total_coverage" + ".html"
    file_path = os.path.join(output_dir, file_name)

    # Add rows to the table
    for _, row in low_coverage_modules.iterrows():
        html_content += f"""
        <tr>
            <td>{row['container']}</td>
            <td>{row['module']}</td>
            <td><a href="{row['file_path']}">{row['file_path']}</a></td>
            <td>{row['coverage']:.2f}%</td>
        </tr>
        """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)


def create_low_coverage_modules_html_report(low_coverage_modules, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    html_content = """
    <html>
    <head>
        <title>Flagged Low Coverage Modules</title>
    </head>
    <body>
        <h1>Flagged Code Coverage Modules</h1>
        <table border="1">
            <thead>
                <tr>
                    <th>Container</th>
                    <th>Module</th>
                    <th>File Path</th>
                    <th>Coverage</th>
                </tr>
            </thead>
            <tbody>
    """
    print(low_coverage_modules)
    file_name = low_coverage_modules["container"].iloc[0] + "_flagged_low_coverage" + ".html"
    file_path = os.path.join(output_dir, file_name)

    # Add rows to the table
    for _, row in low_coverage_modules.iterrows():
        html_content += f"""
        <tr>
            <td>{row['container']}</td>
            <td>{row['module']}</td>
            <td><a href="{row['file_path']}">{row['file_path']}</a></td>
            <td>{row['coverage']:.2f}%</td>
        </tr>
        """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)


def create_container_level_coverage_report(df, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    html_content = """
    <html>
    <head>
        <title>Container-level Code Coverage Report</title>
    </head>
    <body>
        <h1>Container-level Code Coverage Report</h1>
        <table border="1">
                <thead>
                    <tr>
                        <th>Container</th>
                        <th>Detailed Report per Module</th>
                        <th>Module with Low Coverage</th>
                        <th>Total Coverage</th>
                    </tr>
                </thead>
                <tbody>
    """
    file_name = "aggregated_coverage_reports.html"
    file_path = os.path.join(output_dir, file_name)

    # Add rows to the table
    for _, row in df.iterrows():
        html_content += f"""
                <tr>
                    <td>{row['container']}</td>
                    <td><a href="{row['container'] + "_" + "total_coverage" + ".html"}">{row['container'] + "_" + "total_coverage" + ".html"}</a></td>
                    <td><a href="{row['container'] + "_" + "flagged_low_coverage" + ".html"}">{row['container'] + "_" + "flagged_low_coverage" + ".html"}</a></td>
                    <td>{row['total_coverage']:.2f}%</td>
                </tr>
        """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)

def aggregate_overall_coverage(df, output_dir):
    grouped_df = df.groupby("container").agg(
        total_statements=("statements", "sum"),
        total_missing=("missing", "sum")
    ).reset_index()

    # Now calculate total_coverage after aggregation
    grouped_df["total_coverage"] = (grouped_df["total_statements"] - grouped_df["total_missing"]) / grouped_df["total_statements"] * 100

    create_container_level_coverage_report(grouped_df, output_dir)


def aggregate_data_per_container(df, container, output_dir):
    # Filter the DataFrame to only include rows where `container` is 'nvidia_tao_pytorch'
    filtered_df = df[df["container"] == container]

    # Check for low coverage
    low_coverage_modules = []
    all_modules = []

    # Group by 'container', 'module', and 'filepath' and aggregate the sums for 'statements', 'missing', and 'coverage'
    grouped_df = (
        filtered_df.groupby(["container", "module", "other_file_path", "file_reference"])
        .agg(
            total_statements=("statements", "sum"),
            total_missing=("missing", "sum"),
            total_coverage=("coverage", "sum"),
        )
        .reset_index()
    )

    # grouped_df["file_reference"] = df["file_reference"]

    # Group the DataFrame by 'container' and 'module'
    grouped = grouped_df.groupby(["container", "module"])

    # Create an empty list to hold the DataFrames
    dataframes_list = []

    # Iterate over each group and create a DataFrame for each unique module per container
    for (container, module), group in grouped:
        # Create a separate DataFrame for the current container and module
        module_df = group.reset_index(drop=True)  # Reset index for clean DataFrame
        total_row = pd.DataFrame(
            [
                {
                    "container": "Total",
                    "module": "",
                    "other_file_path": "",
                    "total_statements": "",
                    "total_missing": "",
                    "total_coverage": (
                        group["total_statements"].sum() - group["total_missing"].sum()
                    )
                    / group["total_statements"].sum()
                    * 100,
                }
            ]
        )
        
        if total_row["total_coverage"].iloc[0] < 80:
            low_coverage_modules.append({"container": container, "module": module, "coverage": total_row["total_coverage"].iloc[0], "file_path": container.split("_")[-1] + "/" + container + "_" + module.replace("/", "_") + ".html"})

        all_modules.append({"container": container, "module": module, "coverage": total_row["total_coverage"].iloc[0], "file_path": container.split("_")[-1] + "/" + container + "_" + module.replace("/", "_") + ".html"})

        module_df = pd.concat([module_df, total_row], ignore_index=True)
        dataframes_list.append(module_df)

    for df_table in dataframes_list:
        create_html_report_per_container_and_module(df_table, output_dir + "/" + container.split("_")[-1])

    # Create low coverage modules HTML report
    create_low_coverage_modules_html_report(pd.DataFrame(low_coverage_modules), output_dir)

    # Create all coverage modules HTML report
    create_all_modules_per_container_html_report(pd.DataFrame(all_modules), output_dir)


# Main script
html_file = "htmlcov/index.html"  # Replace with your input HTML file

# Parse the HTML and aggregate data
df = parse_html(html_file)

aggregate_data_per_container(df, "nvidia_tao_pytorch", os.path.join(os.path.expanduser("~"), "code_coverage_hosting" , "coverage_reports"))
aggregate_data_per_container(df, "nvidia_tao_deploy", os.path.join(os.path.expanduser("~"), "code_coverage_hosting" , "coverage_reports"))
aggregate_data_per_container(df, "nvidia_tao_ds", os.path.join(os.path.expanduser("~"), "code_coverage_hosting" , "coverage_reports"))
aggregate_data_per_container(df, "nvidia_tao_tf2", os.path.join(os.path.expanduser("~"), "code_coverage_hosting" , "coverage_reports"))

aggregate_overall_coverage(df, os.path.join(os.path.expanduser("~"), "code_coverage_hosting" , "coverage_reports"))
