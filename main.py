import io
import base64
import qrcode

from flask import Flask, render_template, request,make_response, send_file
from PIL import Image
from io import BytesIO
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import SquareModuleDrawer
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.moduledrawers import VerticalBarsDrawer
from qrcode.image.styles.moduledrawers import HorizontalBarsDrawer


def render_code(value, module_drawer='default', resolution='default', size=5, fill_color='black', back_color='white'):
    drawerlist = {
        'default': SquareModuleDrawer(),
        'gapped': GappedSquareModuleDrawer(),
        'circle': CircleModuleDrawer(),
        'rounded': RoundedModuleDrawer(),
        'vertical': VerticalBarsDrawer(),
        'horizontal': HorizontalBarsDrawer()
    }

    resolutionlist = {
        'default': '100',
        'very low': '10',
        'low': '50',
        'high': '150',
        'very high': '250'
    }

    drawer = drawerlist[module_drawer]
    emb_img = None
    qr = qrcode.QRCode(
        version=size,
        box_size=resolutionlist[resolution],
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=1
    )
    qr.add_data(value)
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=drawer,
        embeded_image_path=emb_img,
        back_color=back_color,
        fill_color=fill_color
    )
    img_mem = io.BytesIO()
    img.save(img_mem, "PNG")
    encoded_img_mem = base64.b64encode(img_mem.getvalue())

    return encoded_img_mem.decode("utf-8")


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/preview', methods=['GET', 'POST'])
def code():
    value = request.form['value_input']
    design = request.form['design_input']
    resolution = request.form['resolution_input']
    size = request.form['size_input']
    try:
        size = int(size)
        if not 1 <= size <= 40:
            size = 5
    except ValueError:
        size = 5
    img_data = render_code(value, design, resolution, size)
    return render_template('index.html',
                           preview_value=value,
                           preview_design=design,
                           preview_resolution=resolution,
                           preview_size=size,
                           user_image=img_data
                           )


@app.route('/download', methods=['GET', 'POST'])
def download():
    value = request.form['value_input']
    design = request.form['design_input']
    resolution = request.form['resolution_input']
    size = request.form['size_input']
    try:
        size = int(size)
        if not 1 <= size <= 40:
            size = 5
    except ValueError:
        size = 5
    img_data = render_code(value, design, resolution, size)
    img = Image.open(BytesIO(base64.b64decode(img_data)))
    return


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)



