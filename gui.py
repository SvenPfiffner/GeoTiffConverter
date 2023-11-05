import GeoTIFFConverter as tiff
import gradio as gr

def visualize_tif(tiff_raw):
    data = tiff.GeoTiff(tiff_raw[0])
    return data.visualize()

def generate_mesh(tiff_raw):
    data = tiff.GeoTiff(tiff_raw[0])
    xyz = tiff.Converter.to_point_cloud(data)
    tiff.MeshUtil.point_cloud_to_mesh(xyz, "/data/mesh.obj", downsample_voxel_size=20)

with gr.Blocks() as demo:

    # Single Image Tab
    with gr.Tab("swissALTI3D"):
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
                mesh_button = gr.Button("Generate Mesh")
                mesh_output = gr.Plot()


    visualization_button.click(fn=visualize_tif, inputs=[input_tiffs], outputs=visualization_output)
    mesh_button.click(fn=generate_mesh, inputs=[input_tiffs], outputs=mesh_output)

demo.launch()