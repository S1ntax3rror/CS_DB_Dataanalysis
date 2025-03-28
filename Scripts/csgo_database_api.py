from flask import Flask, render_template, request, session, redirect, url_for, g, jsonify, make_response, send_from_directory

from database import Database
from psycopg.rows import dict_row

db = Database(host='csgodatabase', port=5432)
app = Flask(__name__)
baseroute = '/v1/csgodatabase'

@app.route('/test')
def test():
    return jsonify({'message': 'Successful Connection'})

@app.post(f'{baseroute}/cosmetic')
def add_cosmetic():
    data = request.get_json()

    keys = data.keys()
    if 'name' not in keys:
        return jsonify({'Error': 'Missing name value'}), 400
    if 'type' not in keys:
        return jsonify({'Error': 'Missing type value'}), 400
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT MAX(cosmeticid) FROM Cosmetic")
        cosmeticid = cur.fetchone()[0]
        new_cosmetic_id = cosmeticid + 1
        cur.execute(
            """
            INSERT INTO Cosmetic (cosmeticid, Name, Type) 
            VALUES (%(cosmeticid)s, %(name)s, %(type)s)
            """, {'cosmeticid': new_cosmetic_id, 'name': data['name'], 'type': data['type']}
        )
        db.conn.commit()
        return jsonify({'message': 'Insert successful', 'cosmeticid': new_cosmetic_id})
    except Exception as E:
        return jsonify({'error': E})


@app.get(f'{baseroute}/cosmetic/<int:id>')
def get_cosmetic(id: int):
    cur = db.conn.cursor(row_factory=dict_row)
    cur.execute("""
        SELECT * FROM Cosmetic WHERE CosmeticID = %(id)s
    """, {'id': id})
    result = cur.fetchone()
    if result is None:
        return jsonify({'error': f'CosmeticID doesnt exist - {id}'})
    return jsonify(result)

@app.delete(f'{baseroute}/cosmetic/<int:id>')
def delete_cosmetic(id: int):
    try:
        cur = db.conn.cursor()
        cur.execute("""
            DELETE FROM Cosmetic WHERE CosmeticID = %(id)s
        """, {'id': id})
        db.conn.commit()
    except Exception as E:
        return jsonify({'error': E})
    return jsonify({'message': 'Delete successful'})

@app.put(f'{baseroute}/cosmetic/<int:id>')
def update_cosmetic(id: int):
    Name = None
    Type = None
    data = request.get_json()

    keys = data.keys()

    if 'name' in keys:
        Name = data['name']
    if 'type' in keys:
        Type = data['type']
    try:
        cur = db.conn.cursor(row_factory=dict_row)
        cur.execute("""
            UPDATE Cosmetic SET name = COALESCE(%(name)s, name), type = COALESCE(%(type)s, type) WHERE CosmeticID = %(id)s
        """, {'name': Name, 'type': Type, 'id': id})
        db.conn.commit()
        cur.execute("SELECT * FROM Cosmetic WHERE cosmeticid = %(id)s", {'id': id})
        result = cur.fetchone()
        return jsonify({'message': 'Update successful'} | result)
    except Exception as E:
        return jsonify({'error': E})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)