from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from database import db
from models import Alumno
import os

manage_students = Blueprint('manage_students', __name__)

UPLOAD_FOLDER = '/ruta/a/guardar'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear el directorio si no existe

@manage_students.route('/alumnos', methods=['POST'])
def crear_alumno():
    data = request.form
    usuario_id = data.get('usuario_id')
    if not usuario_id or usuario_id == '':
        usuario_id = 1  # Valor predeterminado válido para `usuario_id`
    
    # Manejo de archivos
    certificado_preparatoria = request.files['certificado_preparatoria']
    curp = data['curp']
    comprobante_pago = request.files['comprobante_pago']

    certificado_filename = secure_filename(certificado_preparatoria.filename)
    certificado_preparatoria.save(os.path.join(UPLOAD_FOLDER, certificado_filename))

    comprobante_filename = secure_filename(comprobante_pago.filename)
    comprobante_pago.save(os.path.join(UPLOAD_FOLDER, comprobante_filename))

    nuevo_alumno = Alumno(
        usuario_id=usuario_id,
        matricula=data['matricula'],
        nombre=data['nombre'],
        domicilio=data.get('domicilio', ''),
        telefono=data.get('telefono', ''),
        correo_electronico=data['correo_electronico'],
        estatus=data.get('estatus', 'Activo'),
        carrera=data['carrera'],
        certificado_preparatoria=certificado_filename,
        curp=curp,
        comprobante_pago=comprobante_filename
    )
    db.session.add(nuevo_alumno)
    db.session.commit()
    flash('Alumno creado con éxito', 'success')
    return redirect(url_for('manage_students.alumnos_web'))

@manage_students.route('/alumnos_web')
def alumnos_web():
    alumnos = Alumno.query.all()
    return render_template('alumnos.html', alumnos=alumnos)

@manage_students.route('/agregar_alumno')
def agregar_alumno():
    return render_template('add_student.html')

@manage_students.route('/alumnos', methods=['GET'])
def obtener_alumnos():
    alumnos = Alumno.query.all()
    output = []
    for alumno in alumnos:
        alumno_data = {
            'id': alumno.id,
            'usuario_id': alumno.usuario_id,
            'matricula': alumno.matricula,
            'nombre': alumno.nombre,
            'domicilio': alumno.domicilio,
            'telefono': alumno.telefono,
            'correo_electronico': alumno.correo_electronico,
            'estatus': alumno.estatus,
            'carrera': alumno.carrera,
            'certificado_preparatoria': alumno.certificado_preparatoria,
            'curp': alumno.curp,
            'comprobante_pago': alumno.comprobante_pago
        }
        output.append(alumno_data)
    return jsonify({"alumnos": output})

@manage_students.route('/alumnos/<int:id>/edit', methods=['GET', 'POST'])
def editar_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    if request.method == 'POST':
        data = request.form
        alumno.usuario_id = data['usuario_id']
        alumno.matricula = data['matricula']
        alumno.nombre = data['nombre']
        alumno.domicilio = data['domicilio']
        alumno.telefono = data['telefono']
        alumno.correo_electronico = data['correo_electronico']
        alumno.estatus = data['estatus']
        alumno.carrera = data['carrera']
        
        if 'certificado_preparatoria' in request.files:
            certificado_preparatoria = request.files['certificado_preparatoria']
            if certificado_preparatoria:
                certificado_filename = secure_filename(certificado_preparatoria.filename)
                certificado_preparatoria.save(os.path.join(UPLOAD_FOLDER, certificado_filename))
                alumno.certificado_preparatoria = certificado_filename
        
        alumno.curp = data['curp']
        
        if 'comprobante_pago' in request.files:
            comprobante_pago = request.files['comprobante_pago']
            if comprobante_pago:
                comprobante_filename = secure_filename(comprobante_pago.filename)
                comprobante_pago.save(os.path.join(UPLOAD_FOLDER, comprobante_filename))
                alumno.comprobante_pago = comprobante_filename

        db.session.commit()
        flash('Alumno actualizado con éxito', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_student.html', alumno=alumno)

@manage_students.route('/alumnos/<int:id>', methods=['POST'])
def actualizar_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    data = request.form
    alumno.usuario_id = data['usuario_id']
    alumno.matricula = data['matricula']
    alumno.nombre = data['nombre']
    alumno.domicilio = data['domicilio']
    alumno.telefono = data['telefono']
    alumno.correo_electronico = data['correo_electronico']
    alumno.estatus = data['estatus']
    alumno.carrera = data['carrera']
    alumno.certificado_preparatoria = data.get('certificado_preparatoria', alumno.certificado_preparatoria)
    alumno.curp = data['curp']
    alumno.comprobante_pago = data.get('comprobante_pago', alumno.comprobante_pago)

    db.session.commit()
    flash('Alumno actualizado con éxito', 'success')
    return redirect(url_for('index'))

@manage_students.route('/alumnos/<id>', methods=['DELETE'])
def eliminar_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    db.session.delete(alumno)
    db.session.commit()
    return jsonify({"mensaje": "Alumno eliminado con éxito"})
