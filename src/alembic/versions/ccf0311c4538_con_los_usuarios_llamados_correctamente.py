"""con los usuarios llamados correctamente

Revision ID: ccf0311c4538
Revises: 9d71b0ec24fc
Create Date: 2024-06-15 10:12:10.518754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccf0311c4538'
down_revision: Union[str, None] = '9d71b0ec24fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_metodos_envios_descripcion', table_name='metodos_envios')
    op.drop_index('ix_metodos_envios_nombre', table_name='metodos_envios')
    op.drop_table('metodos_envios')
    op.drop_index('ix_tipos_compras_descripcion', table_name='tipos_compras')
    op.drop_index('ix_tipos_compras_nombre', table_name='tipos_compras')
    op.drop_table('tipos_compras')
    op.drop_index('ix_estados_compras_descripcion', table_name='estados_compras')
    op.drop_index('ix_estados_compras_nombre', table_name='estados_compras')
    op.drop_table('estados_compras')
    op.drop_index('ix_metodos_pagos_descripcion', table_name='metodos_pagos')
    op.drop_index('ix_metodos_pagos_nombre', table_name='metodos_pagos')
    op.drop_table('metodos_pagos')
    op.drop_index('ix_estados_cotizacion_descripcion', table_name='estados_cotizacion')
    op.drop_index('ix_estados_cotizacion_nombre', table_name='estados_cotizacion')
    op.drop_table('estados_cotizacion')
    op.drop_index('ix_estados_caracteristicas_descripcion', table_name='estados_caracteristicas')
    op.drop_index('ix_estados_caracteristicas_nombre', table_name='estados_caracteristicas')
    op.drop_table('estados_caracteristicas')
    op.drop_index('ix_categorias_descripcion', table_name='categorias')
    op.drop_index('ix_categorias_nombre', table_name='categorias')
    op.drop_table('categorias')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categorias',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_categorias_nombre', 'categorias', ['nombre'], unique=False)
    op.create_index('ix_categorias_descripcion', 'categorias', ['descripcion'], unique=False)
    op.create_table('estados_caracteristicas',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_estados_caracteristicas_nombre', 'estados_caracteristicas', ['nombre'], unique=False)
    op.create_index('ix_estados_caracteristicas_descripcion', 'estados_caracteristicas', ['descripcion'], unique=False)
    op.create_table('estados_cotizacion',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_estados_cotizacion_nombre', 'estados_cotizacion', ['nombre'], unique=False)
    op.create_index('ix_estados_cotizacion_descripcion', 'estados_cotizacion', ['descripcion'], unique=False)
    op.create_table('metodos_pagos',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_metodos_pagos_nombre', 'metodos_pagos', ['nombre'], unique=False)
    op.create_index('ix_metodos_pagos_descripcion', 'metodos_pagos', ['descripcion'], unique=False)
    op.create_table('estados_compras',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_estados_compras_nombre', 'estados_compras', ['nombre'], unique=False)
    op.create_index('ix_estados_compras_descripcion', 'estados_compras', ['descripcion'], unique=False)
    op.create_table('tipos_compras',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tipos_compras_nombre', 'tipos_compras', ['nombre'], unique=False)
    op.create_index('ix_tipos_compras_descripcion', 'tipos_compras', ['descripcion'], unique=False)
    op.create_table('metodos_envios',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nombre', sa.VARCHAR(), nullable=True),
    sa.Column('descripcion', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_metodos_envios_nombre', 'metodos_envios', ['nombre'], unique=False)
    op.create_index('ix_metodos_envios_descripcion', 'metodos_envios', ['descripcion'], unique=False)
    # ### end Alembic commands ###
