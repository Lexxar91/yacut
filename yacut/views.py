from flask import Response, flash, redirect, render_template, request

from . import app, db
from .constants import YOUR_NEW_SHORT_LINK
from .error_handlers import check_short_link
from .forms import UrlMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def main_page():
    """
    Отображает главную страницу сайта и обрабатывает отправленную форму.

    Returns:
        Если форма не прошла валидацию, возвращает HTML-шаблон страницы с формой.
        Если форма прошла валидацию, создает экземпляр класса URLMap, добавляет его в базу данных
        и выводит пользователю новую сокращенную ссылку.
    """
    form = UrlMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = URLMap.get_unique_short_id()
        if check_short_link(custom_id):
            form.custom_id.errors = [f'Имя {custom_id} уже занято!']
            return render_template('yacut.html', form=form)
        urlmap = URLMap(
            original=form.original_link.data,
            short=custom_id,
        )
        db.session.add(urlmap)
        db.session.commit()
        flash(f'{YOUR_NEW_SHORT_LINK}'
              f'<a href="{request.base_url}{custom_id}">'
              f'{request.base_url}{custom_id}</a>')
    return render_template('yacut.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_to_short_link(short) -> Response:
    """
    Перенаправляет пользователя по короткой ссылке на страницу оригинальной ссылки.

    Args:
        short: Короткая ссылка, по которой необходимо перенаправить пользователя.

    Returns:
        Перенаправляет пользователя на страницу оригинальной ссылки, сохраненной в базе данных.
    """
    return redirect(URLMap.query.filter_by(short=short).first_or_404().original)
