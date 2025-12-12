import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import client from '../api/client'

const Projects = () => {
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false)

    const [newProject, setNewProject] = useState({
        name: '',
        key: '',
        description: ''
    })
    useEffect(() => {
        fetchProjects();
    }, [])

    const fetchProjects = async () => {
        try {
            const res = await client.get('/projects')
            setProjects(res.data)

        } catch (err) {
            console.error(err)

        } finally {
            setLoading(false)
        }
    }

    const handleCreate = async e => {

        e.preventDefault()

        try {
            await client.post('/projects', newProject)

            setShowModal(false)
            setNewProject({ name: '', key: '', description: '' })

            fetchProjects()

        } catch (err) {
            alert('Failed to create project')
        }
    }
    if (loading) return <div className="spinner" />


    return (
        <div className="container">

            <div
                style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: 20
                }}
            >
                <h1>Projects</h1>

                <button
                    className="btn btn-primary"
                    onClick={() => setShowModal(true)}
                >
                    Create Project
                </button>
            </div>



            {showModal && (
                <div className="card">

                    <h3>New Project</h3>

                    <form onSubmit={handleCreate}>

                        <input
                            required
                            placeholder="Project Name"
                            value={newProject.name}
                            onChange={e =>
                                setNewProject({ ...newProject, name: e.target.value })
                            }
                        />

                        <input
                            required
                            placeholder="Key (e.g. IH)"
                            value={newProject.key}
                            onChange={e =>
                                setNewProject({ ...newProject, key: e.target.value })
                            }
                        />

                        <textarea
                            placeholder="Description"
                            value={newProject.description}
                            onChange={e =>
                                setNewProject({ ...newProject, description: e.target.value })
                            }
                        />

                        <button type="submit" className="btn btn-primary">
                            Save
                        </button>

                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={() => setShowModal(false)}
                            style={{ marginLeft: 10 }}
                        >
                            Cancel
                        </button>

                    </form>

                </div>
            )}
            <div className="card">
                {projects.length === 0 ? (
                    <p>No projects found.</p>
                ) : (
                    <table className="table-list">
                        <thead>
                            <tr className="table-list-header">
                                <th className="table-list-cell">Name</th>
                                <th className="table-list-cell">Key</th>
                                <th className="table-list-cell">Description</th>
                            </tr>
                        </thead>

                        <tbody>

                            {projects.map(p => (
                                <tr key={p.id} className="table-list-row">

                                    <td className="table-list-cell">
                                        <Link to={`/projects/${p.id}`}>
                                            {p.name}
                                        </Link>
                                    </td>

                                    <td className="table-list-cell">{p.key}</td>

                                    <td className="table-list-cell">
                                        {p.description}
                                    </td>

                                </tr>
                            ))}

                        </tbody>

                    </table>
                )}

            </div>

        </div>
    )
}

export default Projects
