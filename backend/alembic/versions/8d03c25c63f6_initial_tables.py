
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifier
revision: str = '8d03c25c63f6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    
    # table for projects  
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(),    nullable=False),
        sa.Column('name', sa.String(),   nullable=False),
        sa.Column('key',  sa.String(),   nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_projects_id'),
                    'projects',
                    ['id'],
                    unique=False)

    op.create_index(op.f('ix_projects_key'),
                    'projects',
                    ['key'],
                    unique=True)


    # user table  
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(),           nullable=False),
        sa.Column('email', sa.String(),         nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('name', sa.String(),          nullable=True),
        sa.Column('created_at', sa.DateTime(),  nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'),    'users', ['id'],    unique=False)



    # issues  
    op.create_table(
        'issues',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        
        sa.Column('status',
                  sa.Enum('open', 'in_progress', 'resolved', 'closed',
                          name='issuestatus'),
                  nullable=True),

        sa.Column('priority',
                  sa.Enum('low', 'medium', 'high', 'critical',
                          name='priority'),
                  nullable=True),

        sa.Column('reporter_id', sa.Integer(),  nullable=True),
        sa.Column('assignee_id', sa.Integer(),  nullable=True),
        sa.Column('created_at',  sa.DateTime(), nullable=True),
        sa.Column('updated_at',  sa.DateTime(), nullable=True),

        sa.ForeignKeyConstraint(['assignee_id'], ['users.id']),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['reporter_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_issues_id'), 'issues', ['id'], unique=False)



    # project-member-list 
    op.create_table(
        'project_members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('user_id',    sa.Integer(), nullable=True),
        sa.Column('role', sa.Enum('maintainer', 'member', name='role'),
                  nullable=True),

        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['user_id'],    ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_project_members_id'),
                    'project_members',
                    ['id'],
                    unique=False)



    # comments  
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('issue_id',  sa.Integer(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.Column('body',      sa.Text(),    nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),

        sa.ForeignKeyConstraint(['author_id'], ['users.id']),
        sa.ForeignKeyConstraint(['issue_id'],  ['issues.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_comments_id'),
                    'comments',
                    ['id'],
                    unique=False)



def downgrade() -> None:
    
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')

    op.drop_index(op.f('ix_project_members_id'), table_name='project_members')
    op.drop_table('project_members')

    op.drop_index(op.f('ix_issues_id'), table_name='issues')
    op.drop_table('issues')

    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

    op.drop_index(op.f('ix_projects_key'), table_name='projects')
    op.drop_index(op.f('ix_projects_id'),  table_name='projects')
    op.drop_table('projects')
