import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import client from '../api/client'

const ProjectDetail = () => {

    const { id } = useParams()

    const [project, setProject] = useState(null);
    const [issues, setIssues] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);

    const [newIssue, setNewIssue] = useState({
        title: '',
        description: '',
        priority: 'medium',
        status: 'open'
    })
    const [filterStatus, setFilterStatus] = useState('')


    useEffect(() => {

        const fetchData = async () => {

            try {
                const pRes = await client.get(`/projects/${id}`)
                const iRes = await client.get(`/projects/${id}/issues`)

                setProject(pRes.data)
                setIssues(iRes.data)

            } catch (err) {
                console.error(err)

            } finally {
                setLoading(false)
            }
        }

        fetchData()

    }, [id]);



    const handleCreateIssue = async e => {
        e.preventDefault()
        try {
            await client.post(`/projects/${id}/issues`, newIssue)

            setShowModal(false)
            setNewIssue({
                title: '',
                description: '',
                priority: 'medium',
                status: 'open'
            })

            const refreshed = await client.get(`/projects/${id}/issues`)
            setIssues(refreshed.data)

        } catch (err) {
            alert('Failed to create issue')
        }
    }



    const filteredIssues = filterStatus ? issues.filter(i => i.status === filterStatus) : issues
    if (loading) return <div className="spinner" />
    if (!project) return <div>Project not found</div>

    return (
        <div className="container">
            <Link to="/projects" className="btn btn-secondary" style={{ marginBottom: 20 }}>
                &larr; Back to Projects
            </Link>

            <div className="card">
                <h2>
                    {project.name}
                    <span style={{ fontSize: 14, color: '#666' }}>
                        &nbsp;({project.key})
                    </span>
                </h2>

                <p>{project.description}</p>
            </div>



            <div
                style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: 10
                }}
            >

                <div>
                    <label style={{ marginRight: 10 }}>
                        Filter Status:
                    </label>

                    <select
                        value={filterStatus}
                        onChange={e => setFilterStatus(e.target.value)}
                        style={{ width: 'auto' }}
                    >
                        <option value="">All</option>
                        <option value="open">Open</option>
                        <option value="in_progress">In progress</option>
                        <option value="resolved">Resolved</option>
                        <option value="closed">Closed</option>
                    </select>
                </div>

                <button
                    className="btn btn-primary"
                    onClick={() => setShowModal(true)}
                >
                    New issue
                </button>

            </div>



            {showModal && (
                <div className="card">
                    <h3>Create issue</h3>

                    <form onSubmit={handleCreateIssue}>

                        <input
                            required
                            placeholder="Title"
                            value={newIssue.title}
                            onChange={e => setNewIssue({ ...newIssue, title: e.target.value })}
                        />

                        <textarea
                            placeholder="Description"
                            value={newIssue.description}
                            onChange={e => setNewIssue({ ...newIssue, description: e.target.value })}
                        />

                        <select
                            value={newIssue.priority}
                            onChange={e => setNewIssue({ ...newIssue, priority: e.target.value })}
                        >
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                            <option value="critical">Critical</option>
                        </select>

                        <button
                            type="submit"
                            className="btn btn-primary"
                            style={{ marginTop: 10 }}
                        >
                            Create
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

                <table className="table-list">

                    <thead>
                        <tr
                            className="table-list-header"
                            style={{ textAlign: 'center' }}
                        >
                            <th className="table-list-cell">Key</th>
                            <th className="table-list-cell">Title</th>
                            <th className="table-list-cell">Status</th>
                            <th className="table-list-cell">Priority</th>
                            <th className="table-list-cell">Assignee</th>
                        </tr>
                    </thead>

                    <tbody>
                        {filteredIssues.map(issue => (
                            <tr key={issue.id} className="table-list-row">

                                <td className="table-list-cell">
                                    #{issue.id}
                                </td>

                                <td className="table-list-cell">
                                    <Link to={`/issues/${issue.id}`}>
                                        {issue.title}
                                    </Link>
                                </td>

                                <td className="table-list-cell">
                                    <span className={`issue-status-${issue.status}`}>
                                        {issue.status}
                                    </span>
                                </td>

                                <td className="table-list-cell">
                                    {issue.priority}
                                </td>

                                <td className="table-list-cell">
                                    {issue.assignee_id || 'Unassigned'}
                                </td>

                            </tr>
                        ))}
                    </tbody>

                </table>

            </div>

        </div>
    )
}

export default ProjectDetail
