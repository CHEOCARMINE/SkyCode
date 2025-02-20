import os
from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from database import db
from models import Alumno, EstadoAlumno, Carrera

manage_students = Blueprint('manage_students', __name__)

# Asegúrate de que la ruta apunte correctamente al directorio 'uploads' en la raíz del proyecto
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.getcwd(), 'uploads'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear el directorio si no existe
print(f"Directorio de carga: {UPLOAD_FOLDER}")

import os
from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from database import db
from models import Alumno, EstadoAlumno, Carrera

manage_students = Blueprint('manage_students', __name__)

# Asegúrate de que la ruta apunte correctamente al directorio 'uploads' en la raíz del proyecto
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.getcwd(), 'uploads'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear el directorio si no existe
print(f"Directorio de carga: {UPLOAD_FOLDER}")

import os
from flask import Blueprint, request, jsonify, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from database import db
from models import Alumno, EstadoAlumno, Carrera

manage_students = Blueprint('manage_students', __name__)

# Asegúrate de que la ruta apunte correctamente al directorio 'uploads' en la raíz del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
upload_folder = os.path.join(current_dir, 'uploads')
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
print(f"Directorio de carga: {upload_folder}")

@manage_students.route('/alumnos', methods=['POST'])
def crear_alumno():
    try:
        data = request.form
        print(f"Datos recibidos: {data}")

        # Verificar cada campo individualmente
        matricula = data.get('matricula')
        nombre = data.get('nombre')
        domicilio = data.get('domicilio', '')
        telefono = data.get('telefono', '')
        correo_electronico = data.get('correo_electronico')
        curp = data.get('curp')
        estado_id = data.get('estado_id')
        carrera_id = data.get('carrera_id')

        # Asegurarse de que no falte ningún campo requerido
        if not (matricula and nombre and correo_electronico and curp and estado_id and carrera_id):
            raise ValueError("Faltan campos requeridos")

        print(f"matricula: {matricula}")
        print(f"nombre: {nombre}")
        print(f"domicilio: {domicilio}")
        print(f"telefono: {telefono}")
        print(f"correo_electronico: {correo_electronico}")
        print(f"curp: {curp}")
        print(f"estado_id: {estado_id}")
        print(f"carrera_id: {carrera_id}")

        # Manejo de archivos, pero no guardar en la base de datos
        if 'certificado_preparatoria' in request.files:
            certificado_preparatoria = request.files['certificado_preparatoria']
            certificado_filename = secure_filename(certificado_preparatoria.filename)
            certificado_preparatoria.save(os.path.join(upload_folder, certificado_filename))
            print(f"Certificado de preparatoria guardado en: {os.path.join(upload_folder, certificado_filename)}")

        if 'comprobante_pago' in request.files:
            comprobante_pago = request.files['comprobante_pago']
            comprobante_filename = secure_filename(comprobante_pago.filename)
            comprobante_pago.save(os.path.join(upload_folder, comprobante_filename))
            print(f"Comprobante de pago guardado en: {os.path.join(upload_folder, comprobante_filename)}")

        nuevo_alumno = Alumno(
            matricula=matricula,
            nombre=nombre,
            domicilio=domicilio,
            telefono=telefono,
            correo_electronico=correo_electronico,
            curp=curp,
            estado_id=estado_id,
            carrera_id=carrera_id
        )
        print(f"Datos del nuevo alumno: {nuevo_alumno}")

        db.session.add(nuevo_alumno)
        db.session.commit()
        flash('Alumno creado con éxito', 'success')
        return redirect(url_for('index'))
    except ValueError as ve:
        db.session.rollback()
        print(f"ValueError al crear alumno: {ve}")
        return jsonify({"error": str(ve)}), 400
    except TypeError as te:
        db.session.rollback()
        print(f"TypeError al crear alumno: {te}")
        return jsonify({"error": str(te)}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error general al crear alumno: {e}")
        return jsonify({"error": str(e)}), 400


@manage_students.route('/alumnos_web')
def alumnos_web():
    alumnos = Alumno.query.all()
    return render_template('alumnos.html', alumnos=alumnos)

@manage_students.route('/agregar_alumno')
def agregar_alumno():
    estados = EstadoAlumno.query.all()
    carreras = Carrera.query.all()
    return render_template('add_student.html', estados=estados, carreras=carreras)

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
            'curp': alumno.curp,
            'estado_id': alumno.estado_id,
            'carrera_id': alumno.carrera_id
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

    try:
        data = request.form
        alumno.matricula = data.get('matricula')
        alumno.nombre = data.get('nombre')
        alumno.domicilio = data.get('domicilio')
        alumno.telefono = data.get('telefono')
        alumno.correo_electronico = data.get('correo_electronico')
        alumno.curp = data.get('curp')
        alumno.estado_id = data.get('estado_id')
        alumno.carrera_id = data.get('carrera_id')

        # Manejo de archivos
        if 'certificado_preparatoria' in request.files:
            certificado_preparatoria = request.files['certificado_preparatoria']
            if certificado_preparatoria:
                certificado_filename = secure_filename(certificado_preparatoria.filename)
                certificado_preparatoria.save(os.path.join(upload_folder, certificado_filename))
                alumno.certificado_preparatoria = certificado_filename
        
        if 'comprobante_pago' in request.files:
            comprobante_pago = request.files['comprobante_pago']
            if comprobante_pago:
                comprobante_filename = secure_filename(comprobante_pago.filename)
                comprobante_pago.save(os.path.join(upload_folder, comprobante_filename))
                alumno.comprobante_pago = comprobante_filename

        db.session.commit()
        flash('Alumno actualizado con éxito', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar alumno: {e}")
        return jsonify({"error": str(e)}), 400

@manage_students.route('/alumnos/<id>', methods=['DELETE'])
def eliminar_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    db.session.delete(alumno)
    db.session.commit()
    return jsonify({"mensaje": "Alumno eliminado con éxito"})
