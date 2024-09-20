import { useState } from "react"



const Comments = ({comments, handleComment, blog}) => {

    const [commented,setComment] = useState('')
   
    const updateComment = (event) => {
        event.preventDefault()
        setComment(event.target.value)
    }

    const pushComment = (event) => {
        event.preventDefault()
        const comment ={
            comments:commented,
            blogId:blog.id
        }
        handleComment(blog,comment)

    }

    return (<div>
        <h2>Comments</h2>
        <form onSubmit={pushComment}>
            <input
            className="comment"
            value={commented}
            onChange={updateComment}
            type="text"
            name="comment"/>
            <button type="submit">New comment</button>
        </form>
         <ul>
        {comments.map(comment =><li key={comment.id}>{comment.comments}</li>
        )}
        </ul>
    </div>)

}

export default Comments