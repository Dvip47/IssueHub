import React, { useEffect, useState, } from 'react'
import { useParams, Link } from 'react-router-dom'
import client from '../api/client'
import { useAuth } from '../context/AuthContext'

const IssueDetail = () => {

    const { id } = useParams();
    const { user } = useAuth();

    const [issue, setIssue] = useState(null);
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState('');
    const [loading, setLoading] = useState(true)



    useEffect(() => {

        const fetchIssue = async () => {
            try {
                const res = await client.get(`/issues/${id}`);
                const comRes = await client.get(`/issues/${id}/comments`);

                setIssue(res.data);
                setComments(comRes.data);

            } catch (err) {
                console.error(err)

            } finally {
                setLoading(false);
            }
        }

        fetchIssue()

    }, [id])



    const handleStatusChange = async e => {

        const newStatus = e.target.value

        try {
            const res = await client.patch(`/issues/${id}`, { status: newStatus })
            setIssue(res.data);

        } catch (err) {
            alert('Failed to update status. Maintainer only?')
        }
    }


    const handleComment = async e => {

        e.preventDefault()

        try {
            await client.post(`/issues/${id}/comments`, { body: newComment })
            setNewComment('')

            const res = await client.get(`/issues/${id}/comments`)
            setComments(res.data)

        } catch (err) {
            alert('Failed to post comment')
        }
    }



    if (loading) return <div className="spinner" />
    if (!issue) return <div>Issue not found</div>



    return (
        <div className="container">
            <Link to={`/projects/${issue.project_id}`} className="btn btn-secondary" style={{ marginBottom: 20 }}>
                &larr; Back to Issue
            </Link>

            <div className="card">

                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <h2>
                        {issue.title}
                        <span style={{ color: '#666' }}>
                            &nbsp;#{issue.id}
                        </span>
                    </h2>

                    <div>
                        <select value={issue.status} onChange={handleStatusChange}>
                            <option value="open">Open</option>
                            <option value="in_progress">In Progress</option>
                            <option value="resolved">Resolved</option>
                            <option value="closed">Closed</option>
                        </select>
                    </div>
                </div>


                <div style={{ marginBottom: 20 }}>
                    <span
                        className={`issue-status-${issue.status}`}
                        style={{ marginRight: 10 }}
                    >
                        {issue.status}
                    </span>
                    <span>
                        Priority: <b>{issue.priority}</b>
                    </span>
                </div>


                <p style={{ whiteSpace: 'pre-wrap' }}>
                    {issue.description}
                </p>

            </div>



            <div className="card">

                <h3>Comments</h3>

                {comments.length === 0 && (
                    <p>No comments yet.</p>
                )}


                {comments.map(c => (
                    <div
                        key={c.id}
                        style={{
                            padding: '10px 0',
                            borderBottom: '1px solid #eee'
                        }}
                    >
                        <div
                            style={{
                                fontSize: 12,
                                color: '#666',
                                marginBottom: 5
                            }}
                        >
                            User {c.author_id} commented&nbsp;
                            on {new Date(c.created_at).toLocaleString()}
                        </div>

                        <div>{c.body}</div>
                    </div>
                ))}



                <form onSubmit={handleComment} style={{ marginTop: 20 }}>

                    <textarea
                        required
                        rows={3}
                        placeholder="Add a comment..."
                        value={newComment}
                        onChange={e => setNewComment(e.target.value)}
                    />

                    <button type="submit" className="btn btn-primary">
                        Comment
                    </button>
                </form>

            </div>

        </div>
    )
}

export default IssueDetail
