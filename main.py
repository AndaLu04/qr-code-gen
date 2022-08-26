import os.path
import pathlib

from flask import Flask, render_template, request
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import SquareModuleDrawer
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.moduledrawers import VerticalBarsDrawer
from qrcode.image.styles.moduledrawers import HorizontalBarsDrawer
from pathlib import Path


def render_code(value, module_drawer='default', resolution='default', size=10, fill_color='black', back_color='white'):
    drawerlist = {
        'default': SquareModuleDrawer(),
        'gapped': GappedSquareModuleDrawer,
        'circle': CircleModuleDrawer,
        'rounded': RoundedModuleDrawer,
        'vertical': VerticalBarsDrawer,
        'horizontal': HorizontalBarsDrawer
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
        moduledrawer=drawer,
        embeded_image_path=emb_img,
        back_color=back_color,
        fill_color=fill_color
    )
    type(img)
    img.save(f'{pathlib.Path().absolute()}/static/img/code.png')
    return True


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/code', methods=['GET', 'POST'])
def code():
    if render_code(request.form['value_input']) is True:
        return render_template('index.html', user_image='/static/img/code.png')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)



