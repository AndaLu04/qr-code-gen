import io
import base64

import qrcode
import waitress
from flask import Flask, render_template, request, send_file
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, \
    RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer


def render_code(value, module_drawer='default', resolution='default', size=5, fill_color='black', back_color='white'):
    drawer_list = {
        'default': SquareModuleDrawer(),
        'gapped': GappedSquareModuleDrawer(),
        'circle': CircleModuleDrawer(),
        'rounded': RoundedModuleDrawer(),
        'vertical': VerticalBarsDrawer(),
        'horizontal': HorizontalBarsDrawer()
    }

    resolution_list = {
        'default': '100',
        'very low': '10',
        'low': '50',
        'high': '150',
        'very high': '250'
    }

    drawer = drawer_list[module_drawer]
    emb_img = None
    qr = qrcode.QRCode(
        version=size,
        box_size=resolution_list[resolution],
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


def get_form_data(value: str, design: str, resolution: str, size: str) -> tuple[str, str, str, int]:
    try:
        size = int(size)
        if size not in range(1, 41):
            size = 5
    except ValueError:
        size = 5
    return value, design, resolution, size


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/preview', methods=['POST'])
def code():
    value, design, resolution, size = get_form_data(request.form['value_input'],
                                                    request.form['design_input'],
                                                    request.form['resolution_input'],
                                                    request.form['size_input'])
    return render_template('index.html',
                           preview_value=value,
                           preview_design=design,
                           preview_resolution=resolution,
                           preview_size=size,
                           user_image=render_code(value, design, resolution, size)
                           )


@app.route('/download', methods=['POST'])
def download():
    value, design, resolution, size = get_form_data(request.form['value_input'],
                                                    request.form['design_input'],
                                                    request.form['resolution_input'],
                                                    request.form['size_input'])
    return send_file(io.BytesIO(base64.b64decode(render_code(value, design, resolution, size))),
                     as_attachment=True,
                     mimetype='image/png',
                     download_name='qr-code.png')


if __name__ == '__main__':
    waitress.serve(app.run(host="0.0.0.0", port=5432, debug=False))
