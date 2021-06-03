# from flask import Flask, request
from flask import Flask
# from flask_restful import Api, Resource, reqparse, abort
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Video(name={self.name}, views={self.views}, likes={self.likes}"

# db.create_all()

video_put_args = reqparse.RequestParser()
# video_put_args.add_argument("name", type=str, help="Name of the video required")
# video_put_args.add_argument("views", type=int, help="Views of the video required")
# video_put_args.add_argument("likes", type=int, help="Likes of the video required")
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video is required", required=True)

# videos = {}

# def abort_if_video_does_not_exist(video_id):
# 	if video_id not in videos:
# 		abort(404, message=f"Video with video id {video_id} does not exist ...") # <- won't execute return statement after if error occurs; keep that in mind!

# def abort_if_video_exists(video_id):
# 	if video_id in videos:
# 		abort(409, message=f"Video with video id {video_id} already exists ...")

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video is required")
video_update_args.add_argument("likes", type=int, help="Likes of the video is required")

resource_fields = {
	'id': fields.Integer,
	'name':fields.String,
	'views':fields.Integer,
	'likes':fields.Integer
}
# Example output:
# {'id':'the id', 'name':'the name of the object instance', ...}

# CRUD operations:
class Video(Resource):
	# Create
	@marshal_with(resource_fields)
	def put(self, video_id):
		# print(request.form)
		# print(request.form["likes"])
		# return {}

		# args = video_put_args.parse_args()
		# return {video_id: args}
		# args = video_put_args.parse_args()
		# videos[video_id] = args
		# return videos[video_id], 201
		# abort_if_video_exists(video_id)
		# args = video_put_args.parse_args()
		# videos[video_id] = args
		# return videos[video_id], 201

		# args = video_put_args.parse_args()
		# video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args["likes"])
		# db.session.add(video)
		# db.session.commit()
		# return video, 201
		args = video_put_args.parse_args()
		result = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args["likes"])
		if result:
			abort(409, message=f"PUT request: Video with video id {video_id} already exsts ...")
		db.session.add(video)
		db.session.commit()
		return video, 201

	# Read
	@marshal_with(resource_fields)
	def get(self, video_id):
		# abort_if_video_does_not_exist(video_id)
		# return videos[video_id]

		# result = VideoModel.query.filter_by(id=video_id).first()
		# return result
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message=f"GET request: Video with video id {video_id} does not exist ...")
		return result

	# Update
	@marshal_with(resource_fields)
	def patch(self, video_id):
		args = video_update_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		# print(result)
		if not result:
			abort(404, message=f"PATCH request: Video with video id {video_id} does not exist ...")
		# if "name" in args and args['name'] not none:
		if args['name']:
			result.name = args['name']
		# if "views" in args:
		if args['views']:
			result.views = args['views']
		# if "likes" in args:
		if args['likes']:
			result.likes = args['likes']
		# db.session.add(result)
		db.session.commit()
		return result, 204

	# Delete
	# @marshal_with(resource_fields)
	def delete(self, video_id):
		# abort_if_video_does_not_exist(video_id)
		# del videos[video_id]
		# return "", 204

		result = VideoModel.query.filter_by(id=video_id).first()
		# print(result)
		if result:
			db.session.delete(result)
			db.session.commit()
			return "", 200
		else:
			abort(404, message=f"DELETE request: Video with video id {video_id} does not exist ...")

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
	app.run(debug=True)