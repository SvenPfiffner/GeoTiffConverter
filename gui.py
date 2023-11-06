import GeoTIFFConverter as tiff
import gradio as gr

def visualize_tif(tiff_raw):
    data = tiff.GeoTiff(tiff_raw[0])
    return data.visualize()

def generate_mesh(tiff_raw, downsample, add_base, height):
    data = tiff.GeoTiff(tiff_raw[0])
    xyz = tiff.Converter.to_point_cloud(data, base_height=height)
    base_flag = True if add_base == "True" else False
    tiff.MeshUtil.point_cloud_to_mesh(xyz, "data/mesh.obj", downsample_voxel_size=downsample, add_base=base_flag)
    return "data/mesh.obj"

def retrieve_geo_data(tiff_raw):
    pass

def retrieve_meta_data(tiff_raw):
    pass

with gr.Blocks() as demo:

    # Elevation tab
    with gr.Tab("Elevation"):
        # Input Tiff
        input_tiffs_elevation = gr.File(label="Input TIFFs", file_count='multiple', file_types=[".tif"])
        # IO
        with gr.Row():
            #Visualization site
            with gr.Column():
                visualization_button = gr.Button("Visualize Elevation Information")
                visualization_output = gr.Plot()
            #Mesh site
            with gr.Column():
                voxel_downsampling = gr.Slider(label="Downsampling strength", minimum=0, maximum=50, value=20, step=1)
                with gr.Row():
                    lowest_height = gr.Number(label="Height of lowest vertex", minimum=0)
                    include_base = gr.Radio(label="Add base to mesh", choices=["True", "False"], value="False")
                mesh_button = gr.Button("Generate Mesh")
                mesh_output = gr.Model3D()

    # Data analysis tab
    with gr.Tab("Data Analysis"):
        # Input Tiff
        input_tiff_analysis = gr.File(label="Input TIFFs", file_count='single', file_types=[".tif"])
        # IO
        with gr.Row():
            #Plotting site
            with gr.Column():
                data_analysis_plots_button = gr.Button("Plot characteristics")
                with gr.Row():
                    gr.Plot()
                    gr.Plot()
                with gr.Row():
                    gr.Plot()
                    gr.Plot()
            with gr.Column():
                data_analysis_geo_button = gr.Button("Retrieve Geo-Information")
                gr.Plot()
                gr.Plot()
            with gr.Column():
                data_analysis_meta_button = gr.Button("Show Metadata")
                gr.Textbox(lines=10)



    visualization_button.click(fn=visualize_tif, inputs=[input_tiffs_elevation], outputs=visualization_output)
    mesh_button.click(fn=generate_mesh, inputs=[input_tiffs_elevation, voxel_downsampling, include_base, lowest_height], outputs=mesh_output)
    data_analysis_geo_button.click(fn=retrieve_geo_data, inputs=[input_tiff_analysis])
    data_analysis_meta_button.click(fn=retrieve_meta_data, inputs=[input_tiff_analysis])

demo.launch()