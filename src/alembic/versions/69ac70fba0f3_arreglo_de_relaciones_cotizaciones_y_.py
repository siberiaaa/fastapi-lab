"""arreglo de relaciones cotizaciones y compras

Revision ID: 69ac70fba0f3
Revises: 0bbf2852b412
Create Date: 2024-06-17 10:17:09.994543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69ac70fba0f3'
down_revision: Union[str, None] = '0bbf2852b412'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_metodos_pagos_descripcion', table_name='metodos_pagos')
    op.drop_index('ix_metodos_pagos_nombre', table_name='metodos_pagos')
    op.drop_table('metodos_pagos')
    op.drop_index('ix_calificaciones_comentario', table_name='calificaciones')
    op.drop_index('ix_calificaciones_emoticono', table_name='calificaciones')
    op.drop_index('ix_calificaciones_estrellas', table_name='calificaciones')
    op.drop_index('ix_calificaciones_titulo', table_name='calificaciones')
    op.drop_table('calificaciones')
    op.drop_index('ix_tipos_usuarios_descripcion', table_name='tipos_usuarios')
    op.drop_index('ix_tipos_usuarios_nombre', table_name='tipos_usuarios')
    op.drop_table('tipos_usuarios')
    op.drop_index('ix_cotizaciones_precio', table_name='cotizaciones')
    op.drop_table('cotizaciones')
    op.drop_index('ix_compras_cantidad', table_name='compras')
    op.drop_index('ix_compras_fecha', table_name='compras')
    op.drop_table('compras')
    op.drop_index('ix_estados_caracteristicas_descripcion', table_name='estados_caracteristicas')
    op.drop_index('ix_estados_caracteristicas_nombre', table_name='estados_caracteristicas')
    op.drop_table('estados_caracteristicas')
    op.drop_index('ix_metodos_envios_descripcion', table_name='metodos_envios')
    op.drop_index('ix_metodos_envios_nombre', table_name='metodos_envios')
    op.drop_table('metodos_envios')
    op.drop_index('ix_anecdotas_descripcion', table_name='anecdotas')
    op.drop_index('ix_anecdotas_nombre', table_name='anecdotas')
    op.drop_table('anecdotas')
    op.drop_index('ix_estados_cotizacion_descripcion', table_name='estados_cotizacion')
    op.drop_index('ix_estados_cotizacion_nombre', table_name='estados_cotizacion')
    op.drop_table('estados_cotizacion')
    op.drop_index('ix_categorias_descripcion', table_name='categorias')
    op.drop_index('ix_categorias_nombre', table_name='categorias')
    op.drop_table('categorias')
    op.drop_index('ix_tipos_compras_descripcion', table_name='tipos_compras')
    op.drop_index('ix_tipos_compras_nombre', table_name='tipos_compras')
    op.drop_table('tipos_compras')
    op.drop_index('ix_reseñas_años_produccion', table_name='reseñas')
    op.drop_index('ix_reseñas_invencion', table_name='reseñas')
    op.drop_index('ix_reseñas_inventor', table_name='reseñas')
    op.drop_table('reseñas')
    op.drop_index('ix_facturas_fecha_entrega', table_name='facturas')
    op.drop_table('facturas')
    op.drop_index('ix_caracteristicas_explicacion', table_name='caracteristicas')
    op.drop_index('ix_caracteristicas_nombre', table_name='caracteristicas')
    op.drop_table('caracteristicas')
    op.drop_index('ix_tipos_productos_descripcion', table_name='tipos_productos')
    op.drop_index('ix_tipos_productos_funcionalidad', table_name='tipos_productos')
    op.drop_index('ix_tipos_productos_nombre', table_name='tipos_productos')
    op.drop_table('tipos_productos')
    op.drop_index('ix_productos_altura_cm', table_name='productos')
    op.drop_index('ix_productos_anchura_cm', table_name='productos')
    op.drop_index('ix_productos_descripcion', table_name='productos')
    op.drop_index('ix_productos_imagen', table_name='productos')
    op.drop_index('ix_productos_nombre', table_name='productos')
    op.drop_index('ix_productos_peso_gramo', table_name='productos')
    op.drop_index('ix_productos_profundidad_cm', table_name='productos')
    op.drop_table('productos')
    op.drop_index('ix_estados_compras_descripcion', table_name='estados_compras')
    op.drop_index('ix_estados_compras_nombre', table_name='estados_compras')
    op.drop_table('estados_compras')
    op.drop_index('ix_usuarios_apellidos', table_name='usuarios')
    op.drop_index('ix_usuarios_contraseña', table_name='usuarios')
    op.drop_index('ix_usuarios_correo', table_name='usuarios')
    op.drop_index('ix_usuarios_direccion', table_name='usuarios')
    op.drop_index('ix_usuarios_nacimiento', table_name='usuarios')
    op.drop_index('ix_usuarios_nombres', table_name='usuarios')
    op.drop_table('usuarios')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuarios',
    sa.Column('cedula', sa.VARCHAR(), nullable=False),
    sa.Column('nombres', sa.VARCHAR(), nullable=True),
    sa.Column('apellidos', sa.VARCHAR(), nullable=True),
    sa.Column('nacimiento', sa.DATETIME(), nullable=True),
    sa.Column('direccion', sa.VARCHAR(), nullable=True),
    sa.Column('correo', sa.VARCHAR(), nullable=True),
    sa.Column('contraseña', sa.VARCHAR(), nullable=True),
    sa.Column('tipo_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['tipo_id'], ['tipos_usuarios.id'], ),
    sa.PrimaryKeyConstraint('cedula')
    )
    op.create_index('ix_usuarios_nombres', 'usuarios', ['nombres'], unique=False)
    op.create_index('ix_usuarios_nacimiento', 'usuarios', ['nacimiento'], unique=False)
    op.create_index('ix_usuarios_direccion', 'usuarios', ['direccion'], unique=False)
    op.create_index('ix_usuarios_correo', 'usuarios', ['correo'], unique=False)
    op.create_index('ix_usuarios_contraseña', 'usuarios', ['contraseña'], unique=False)
    op.create_index('ix_usuarios_apellidos', 'usuarios', ['apellidos'], unique=False)
    op.create_table('estados_compras',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_estados_compras_nombre', 'estados_compras', ['nombre'], unique=False)
    op.create_index('ix_estados_compras_descripcion', 'estados_compras', ['descripcion'], unique=False)
    op.create_table('productos',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.Column('altura_cm', sa.FLOAT(), nullable=True),
    sa.Column('anchura_cm', sa.FLOAT(), nullable=True),
    sa.Column('profundidad_cm', sa.FLOAT(), nullable=True),
    sa.Column('imagen', sa.BLOB(), nullable=True),
    sa.Column('peso_gramo', sa.FLOAT(), nullable=True),
    sa.Column('usuario_cedula', sa.VARCHAR(), nullable=True),
    sa.Column('tipo_producto_id', sa.INTEGER(), nullable=True),
    sa.Column('categoria_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['categoria_id'], ['categorias.id'], ),
    sa.ForeignKeyConstraint(['tipo_producto_id'], ['tipos_productos.id'], ),
    sa.ForeignKeyConstraint(['usuario_cedula'], ['usuarios.cedula'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_productos_profundidad_cm', 'productos', ['profundidad_cm'], unique=False)
    op.create_index('ix_productos_peso_gramo', 'productos', ['peso_gramo'], unique=False)
    op.create_index('ix_productos_nombre', 'productos', ['nombre'], unique=False)
    op.create_index('ix_productos_imagen', 'productos', ['imagen'], unique=False)
    op.create_index('ix_productos_descripcion', 'productos', ['descripcion'], unique=False)
    op.create_index('ix_productos_anchura_cm', 'productos', ['anchura_cm'], unique=False)
    op.create_index('ix_productos_altura_cm', 'productos', ['altura_cm'], unique=False)
    op.create_table('tipos_productos',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.Column('funcionalidad', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tipos_productos_nombre', 'tipos_productos', ['nombre'], unique=False)
    op.create_index('ix_tipos_productos_funcionalidad', 'tipos_productos', ['funcionalidad'], unique=False)
    op.create_index('ix_tipos_productos_descripcion', 'tipos_productos', ['descripcion'], unique=False)
    op.create_table('caracteristicas',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('explicacion', sa.VARCHAR(), nullable=True),
    sa.Column('encargo_id', sa.INTEGER(), nullable=True),
    sa.Column('estado_caracteristica_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['encargo_id'], ['compras.id'], ),
    sa.ForeignKeyConstraint(['estado_caracteristica_id'], ['estados_caracteristicas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_caracteristicas_nombre', 'caracteristicas', ['nombre'], unique=False)
    op.create_index('ix_caracteristicas_explicacion', 'caracteristicas', ['explicacion'], unique=False)
    op.create_table('facturas',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('fecha_entrega', sa.DATETIME(), nullable=True),
    sa.Column('cotizacion_id', sa.INTEGER(), nullable=True),
    sa.Column('metodo_pago_id', sa.INTEGER(), nullable=True),
    sa.Column('metodo_envio_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['cotizacion_id'], ['cotizaciones.id'], ),
    sa.ForeignKeyConstraint(['metodo_envio_id'], ['metodos_envios.id'], ),
    sa.ForeignKeyConstraint(['metodo_pago_id'], ['metodos_pagos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_facturas_fecha_entrega', 'facturas', ['fecha_entrega'], unique=False)
    op.create_table('reseñas',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('invencion', sa.DATETIME(), nullable=True),
    sa.Column('inventor', sa.VARCHAR(), nullable=True),
    sa.Column('años_produccion', sa.INTEGER(), nullable=True),
    sa.Column('producto_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_reseñas_inventor', 'reseñas', ['inventor'], unique=False)
    op.create_index('ix_reseñas_invencion', 'reseñas', ['invencion'], unique=False)
    op.create_index('ix_reseñas_años_produccion', 'reseñas', ['años_produccion'], unique=False)
    op.create_table('tipos_compras',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tipos_compras_nombre', 'tipos_compras', ['nombre'], unique=False)
    op.create_index('ix_tipos_compras_descripcion', 'tipos_compras', ['descripcion'], unique=False)
    op.create_table('categorias',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_categorias_nombre', 'categorias', ['nombre'], unique=False)
    op.create_index('ix_categorias_descripcion', 'categorias', ['descripcion'], unique=False)
    op.create_table('estados_cotizacion',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_estados_cotizacion_nombre', 'estados_cotizacion', ['nombre'], unique=False)
    op.create_index('ix_estados_cotizacion_descripcion', 'estados_cotizacion', ['descripcion'], unique=False)
    op.create_table('anecdotas',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.Column('reseña_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['reseña_id'], ['reseñas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_anecdotas_nombre', 'anecdotas', ['nombre'], unique=False)
    op.create_index('ix_anecdotas_descripcion', 'anecdotas', ['descripcion'], unique=False)
    op.create_table('metodos_envios',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_metodos_envios_nombre', 'metodos_envios', ['nombre'], unique=False)
    op.create_index('ix_metodos_envios_descripcion', 'metodos_envios', ['descripcion'], unique=False)
    op.create_table('estados_caracteristicas',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_estados_caracteristicas_nombre', 'estados_caracteristicas', ['nombre'], unique=False)
    op.create_index('ix_estados_caracteristicas_descripcion', 'estados_caracteristicas', ['descripcion'], unique=False)
    op.create_table('compras',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('cantidad', sa.INTEGER(), nullable=True),
    sa.Column('fecha', sa.DATETIME(), nullable=True),
    sa.Column('cliente_cedula', sa.VARCHAR(), nullable=True),
    sa.Column('producto_id', sa.INTEGER(), nullable=True),
    sa.Column('tipo_compra_id', sa.INTEGER(), nullable=True),
    sa.Column('estado_compra_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_cedula'], ['usuarios.cedula'], ),
    sa.ForeignKeyConstraint(['estado_compra_id'], ['estados_compras.id'], ),
    sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], ),
    sa.ForeignKeyConstraint(['tipo_compra_id'], ['tipos_compras.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_compras_fecha', 'compras', ['fecha'], unique=False)
    op.create_index('ix_compras_cantidad', 'compras', ['cantidad'], unique=False)
    op.create_table('cotizaciones',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('precio', sa.FLOAT(), nullable=True),
    sa.Column('compra_id', sa.INTEGER(), nullable=True),
    sa.Column('estado_cotizacion_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['compra_id'], ['compras.id'], ),
    sa.ForeignKeyConstraint(['estado_cotizacion_id'], ['estados_compras.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_cotizaciones_precio', 'cotizaciones', ['precio'], unique=False)
    op.create_table('tipos_usuarios',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tipos_usuarios_nombre', 'tipos_usuarios', ['nombre'], unique=False)
    op.create_index('ix_tipos_usuarios_descripcion', 'tipos_usuarios', ['descripcion'], unique=False)
    op.create_table('calificaciones',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('titulo', sa.VARCHAR(), nullable=True),
    sa.Column('comentario', sa.VARCHAR(), nullable=True),
    sa.Column('estrellas', sa.INTEGER(), nullable=True),
    sa.Column('emoticono', sa.INTEGER(), nullable=True),
    sa.Column('usuario_cedula', sa.VARCHAR(), nullable=True),
    sa.Column('producto_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], ),
    sa.ForeignKeyConstraint(['usuario_cedula'], ['usuarios.cedula'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_calificaciones_titulo', 'calificaciones', ['titulo'], unique=False)
    op.create_index('ix_calificaciones_estrellas', 'calificaciones', ['estrellas'], unique=False)
    op.create_index('ix_calificaciones_emoticono', 'calificaciones', ['emoticono'], unique=False)
    op.create_index('ix_calificaciones_comentario', 'calificaciones', ['comentario'], unique=False)
    op.create_table('metodos_pagos',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_metodos_pagos_nombre', 'metodos_pagos', ['nombre'], unique=False)
    op.create_index('ix_metodos_pagos_descripcion', 'metodos_pagos', ['descripcion'], unique=False)
    # ### end Alembic commands ###
