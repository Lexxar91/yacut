from http import HTTPStatus
from flask import jsonify, request
from . import app, db
from .constants import NOT_FOUND_ID, MISSING_REQUEST, REQUIRED_FIELD, ERROR_SHORT_URL
from .error_handlers import InvalidAPIUsage, check_short_link
from .models import URLMap
from .utils import check_symbols


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """
    Создает короткую ссылку для указанного URL-адреса или возвращает ошибку, если в запросе нет URL-адреса или
    если пользователь попытался использовать не уникальное имя для короткой ссылки.

    :return: JSON-объект, содержащий информацию о созданной короткой ссылке и код ответа HTTP 201 CREATED.
    :raises InvalidAPIUsage: если в запросе отсутствует тело, нет поля "url" или "custom_id" не уникально,
    либо имя короткой ссылки содержит недопустимые символы.
    """
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(MISSING_REQUEST)

    if 'url' not in data:
        raise InvalidAPIUsage(REQUIRED_FIELD, HTTPStatus.BAD_REQUEST)

    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = URLMap.get_unique_short_id()

    custom_id = data['custom_id']
    if len(custom_id) > 16 or not check_symbols(custom_id):
        raise InvalidAPIUsage(ERROR_SHORT_URL, HTTPStatus.BAD_REQUEST)

    if check_short_link(custom_id):
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.', HTTPStatus.BAD_REQUEST)

    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """
    Возвращает исходный URL-адрес, соответствующий указанной короткой ссылке.

    :param short_id: ID короткой ссылки для поиска.
    :type short_id: str
    :return: JSON-объект, содержащий исходный URL-адрес и код ответа HTTP 200 OK.
    :raises InvalidAPIUsage: если короткая ссылка не найдена в базе данных.
    """
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage(NOT_FOUND_ID, HTTPStatus.NOT_FOUND)
    return jsonify({"url": url.original}), HTTPStatus.OK
