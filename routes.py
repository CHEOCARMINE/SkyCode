from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from database import db, app
from models import Alumno
import os

UPLOAD_FOLDER = '/ruta/a/guardar'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear el directorio si no existe

# Ruta para mostrar la lista de alumnos en HTML
@app.route('/alumnos_web')
def alumnos_web():
    alumnos = Alumno.query.all()
    return render_template('alumnos.html', alumnos=alumnos)

# Ruta para obtener todos los alumnos en JSON
@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    alumnos = Alumno.query.all()
    alumnos_list = [{"id": a.id, "matricula": a.matricula, "nombre": a.nombre,
                     "curp": a.curp, "domicilio": a.domicilio, "telefono": a.telefono,
                     "correo_electronico": a.correo_electronico, "certificado_preparatoria": a.certificado_preparatoria,
                     "comprobante_pago": a.comprobante_pago, "estado_id": a.estado_id, "carrera_id": a.carrera_id} for a in alumnos]
    return jsonify(alumnos_list)

# Ruta para agregar un nuevo alumno
@app.route('/alumnos', methods=['POST'])
def add_alumno():
    data = request.form

    # Manejo de archivos
    certificado_preparatoria = request.files['certificado_preparatoria']
    curp = data['curp']
    comprobante_pago = request.files['comprobante_pago']

    certificado_filename = secure_filename(certificado_preparatoria.filename)
    certificado_preparatoria.save(os.path.join(UPLOAD_FOLDER, certificado_filename))

    comprobante_filename = secure_filename(comprobante_pago.filename)
    comprobante_pago.save(os.path.join(UPLOAD_FOLDER, comprobante_filename))

    nuevo_alumno = Alumno(
        matricula=data['matricula'],
        nombre=data['nombre'],
        curp=curp,
        domicilio=data.get('domicilio', ''),
        telefono=data.get('telefono', ''),
        correo_electronico=data['correo_electronico'],
        certificado_preparatoria=certificado_filename,
        comprobante_pago=comprobante_filename,
        estado_id=data['estado_id'],
        carrera_id=data['carrera_id']
    )
    db.session.add(nuevo_alumno)
    db.session.commit()
    return redirect(url_for('alumnos_web'))

# Ruta para eliminar un alumno
@app.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"mensaje": "Alumno no encontrado"}), 404
    db.session.delete(alumno)
    db.session.commit()
    return jsonify({"mensaje": "Alumno eliminado correctamente"})

# Ruta para actualizar un alumno
@app.route('/alumnos/<int:id>', methods=['PUT'])
def update_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"mensaje": "Alumno no encontrado"}), 404
    data = request.json
    alumno.matricula = data['matricula']
    alumno.nombre = data['nombre']
    alumno.domicilio = data['domicilio']
    alumno.telefono = data['telefono']
    alumno.correo_electronico = data['correo_electronico']
    alumno.curp = data['curp']
    alumno.estado_id = data['estado_id']
    alumno.carrera_id = data['carrera_id']
    alumno.certificado_preparatoria = data.get('certificado_preparatoria', alumno.certificado_preparatoria)
    alumno.comprobante_pago = data.get('comprobante_pago', alumno.comprobante_pago)
    db.session.commit()
    return jsonify({"mensaje": "Alumno actualizado correctamente"})
