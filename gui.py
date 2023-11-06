import GeoTIFFConverter as tiff
import gradio as gr

def visualize_tif(tiff_raw):
    data = tiff.GeoTiff(tiff_raw[0])
    return data.visualize()

def generate_mesh(tiff_raw, downsample):
    data = tiff.GeoTiff(tiff_raw[0])
    xyz = tiff.Converter.to_point_cloud(data)
    tiff.MeshUtil.point_cloud_to_mesh(xyz, "data/mesh.obj", downsample_voxel_size=downsample)
    return "data/mesh.obj"

with gr.Blocks() as demo:

    # Single Image Tab
    with gr.Tab("Elevation-TIFF"):
        # Input Tiff
        input_tiffs = gr.File(label="Input TIFFs", file_count='multiple', file_types=[".tif"])
        # IO
        with gr.Row():
            #Visualization site
            with gr.Column():
                visualization_button = gr.Button("Visualize Height Information")
                visualization_output = gr.Plot()
            #Mesh site
            with gr.Column():
                voxel_downsampling = gr.Slider(minimum=0, maximum=50, value=20, step=1)
                mesh_button = gr.Button("Generate Mesh")
                mesh_output = gr.Model3D()


    visualization_button.click(fn=visualize_tif, inputs=[input_tiffs], outputs=visualization_output)
    mesh_button.click(fn=generate_mesh, inputs=[input_tiffs, voxel_downsampling], outputs=mesh_output)

demo.launch()