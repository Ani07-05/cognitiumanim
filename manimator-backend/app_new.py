from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import subprocess
import os
import shutil
from gtts import gTTS
import time
import uuid
import logging

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})
socketio = SocketIO(app, 
    cors_allowed_origins="*",
    async_mode='threading',
    logger=True,
    engineio_logger=True
)

def sanitize_filename(topic):
    # Convert to lowercase and replace spaces/special chars with underscore
    return "".join(c if c.isalnum() else "_" for c in topic.lower())

def get_visualization_code(topic: str) -> str:
    """Get the appropriate visualization code based on topic."""
    topic_lower = topic.lower()
    
    common_helper_methods = '''
    def create_element(self, value: str, width: float = 1.0) -> VGroup:
        """Create a styled element with value."""
        box = Square(side_length=width, fill_opacity=0.8, fill_color=BLUE)
        text = Text(str(value), font="Fira Code", font_size=24)
        return VGroup(box, text)
    '''
    
    if 'queue' in topic_lower:
        return common_helper_methods + '''
    def visualize_process(self) -> None:
        """Queue operations visualization."""
        title = Text("Queue Operations", font_size=40).to_edge(UP)
        self.play(Write(title))
        
        # Initialize queue
        elements = VGroup()
        elements.arrange(RIGHT, buff=0.1).move_to(ORIGIN)
        
        # Show enqueue operations
        data = ["A", "B", "C", "D"]
        for value in data:
            new_elem = self.create_element(value)
            new_elem.next_to(elements, RIGHT if len(elements) > 0 else ORIGIN)
            
            op_text = Text(f"Enqueue({value})", font="Fira Code", font_size=30, color=YELLOW).to_edge(DOWN)
            self.play(Write(op_text), FadeIn(new_elem, shift=UP))
            elements.add(new_elem)
            
            if len(elements) > 1:
                self.play(elements.animate.arrange(RIGHT, buff=0.1).move_to(ORIGIN))
            self.play(FadeOut(op_text))
        
        self.wait()
        
        # Show dequeue operations
        for i in range(2):
            if len(elements) == 0: break
            
            op_text = Text(f"Dequeue() → {data[i]}", font="Fira Code", font_size=30, color=RED).to_edge(DOWN)
            self.play(Write(op_text))
            
            first = elements[0]
            rest = elements[1:]
            
            self.play(first.animate.set_color(RED))
            self.play(
                FadeOut(first, shift=UP),
                *([rest.animate.arrange(RIGHT, buff=0.1).move_to(ORIGIN)] if len(rest) > 0 else [])
            )
            
            elements = rest
            self.play(FadeOut(op_text))
        
        self.wait()
        self.play(FadeOut(title), FadeOut(elements))
'''
    elif 'tree' in topic_lower or 'bst' in topic_lower:
        return common_helper_methods + '''
    def visualize_process(self) -> None:
        """Binary tree visualization."""
        title = Text("Binary Tree Operations", font_size=40).to_edge(UP)
        self.play(Write(title))
        
        # Create tree visualization
        values = [5, 3, 7, 2, 4, 6, 8]
        nodes = {}
        edges = VGroup()
        
        def add_node(value, position):
            node = VGroup(
                Circle(radius=0.3, fill_opacity=0.8, fill_color=BLUE),
                Text(str(value), font_size=24, color=WHITE)
            )
            node.move_to(position)
            nodes[value] = node
            return node
        
        # Build tree level by level
        level_height = 1
        level_width = 2
        root_pos = UP * 2
        
        # Add root
        root = add_node(values[0], root_pos)
        self.play(Create(root))
        
        # Add remaining nodes
        for i, value in enumerate(values[1:], 1):
            # Calculate position
            level = i // 2
            direction = -1 if value < values[(i-1)//2] else 1
            position = root_pos + DOWN * level_height * level + RIGHT * direction * level_width / (level + 1)
            
            # Create and animate node
            node = add_node(value, position)
            parent = nodes[values[(i-1)//2]]
            edge = Line(parent.get_center(), node.get_center(), color=WHITE)
            edges.add(edge)
            
            self.play(Create(edge), Create(node))
            
        self.wait()
        self.play(FadeOut(title), *[FadeOut(node) for node in nodes.values()], FadeOut(edges))
'''
    else:
        return common_helper_methods + '''
    def visualize_process(self) -> None:
        """Generic data structure visualization."""
        title = Text("Data Structure Operations", font_size=40).to_edge(UP)
        self.play(Write(title))
        
        # Create basic visualization
        elements = VGroup()
        for i in range(5):
            element = self.create_element(str(i))
            elements.add(element)
        
        elements.arrange(RIGHT, buff=0.5)
        self.play(Create(elements))
        
        # Show some operations
        self.wait()
        self.play(
            FadeOut(elements[0], shift=UP),
            elements[1:].animate.arrange(RIGHT, buff=0.5).move_to(ORIGIN)
        )
        
        self.wait()
        self.play(FadeOut(title), FadeOut(elements))
'''

def generate_manim_script(topic):
    # Generate class name from topic
    class_name = "".join(word.capitalize() for word in topic.split())
    filename = f"temp_{sanitize_filename(topic)}_{str(uuid.uuid4())[:8]}"
    
    # Get visualization code based on topic
    visualization_code = get_visualization_code(topic)

    script = f'''from manim import *

config.frame_rate = 60
config.media_width = "1280x720"

class {class_name}Scene(Scene):
    \"""A professional educational animation explaining {topic.title()}.
    
    This scene implements ManimCE v0.18.1+ compatible code and follows 
    professional education video standards.
    \"""
    
    topic: str = "{topic}"
    aspect_ratio = (14, 8)
    tex_template = TexTemplate(tex_compiler="latex")
    
    def construct(self) -> None:
        # Ensure clean slate between scenes
        self.remove(*self.mobjects)
        
        # Scene 1: Title (5-10s)
        self.show_title()
        
        # Scene 2: Core Concept (45-60s) 
        self.explain_concept()
        
        # Scene 3: Visualization (60-90s)
        self.visualize_process()
        
        # Scene 4: Applications (20-30s)
        self.show_applications()
        
        # Clean up at end
        self.play(FadeOut(*self.mobjects))

    def show_title(self) -> None:
        """Animated title sequence with professional typography."""
        title = MathTex(r"\\textsc{{{topic.title()}}}", font_size=48)
        subtitle = Tex(
            "Understanding the Core Concepts",
            tex_template=self.tex_template,
            color=GRAY,
            font_size=36
        )
        
        # Create professional title animation
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.5)
        self.play(
            AnimationGroup(
                DrawBorderThenFill(title),
                Write(subtitle),
                lag_ratio=0.5
            )
        )
        self.wait(2)
        self.play(FadeOut(title_group))

    def explain_concept(self) -> None:
        """Core concept explanation with mathematical foundations."""
        concept_title = Tex("Core Concepts", font_size=40).to_edge(UP)
        
        # Mathematical foundation using proper LaTeX
        equation = MathTex(
            r"\\begin{{cases}}"
            r"\\text{{Time Complexity}} &= \\mathcal{{O}}(n) \\\\"
            r"\\text{{Space Complexity}} &= \\mathcal{{O}}(1)"
            r"\\end{{cases}}",
            tex_template=self.tex_template,
            font_size=36
        ).next_to(concept_title, DOWN)
        
        self.play(
            Write(concept_title),
            FadeIn(equation, shift=UP)
        )
        self.wait(2)
        self.play(FadeOut(concept_title), FadeOut(equation))

{visualization_code}

    def show_applications(self) -> None:
        """Real-world applications with performance analysis."""
        # Create professional comparison table
        applications_title = Text("Practical Applications", font_size=40)
        applications_title.to_edge(UP)
        
        table = Table(
            [["Best Case", r"$\\\mathcal{O}(1)$", "Ideal condition"],
             ["Average", r"$\\mathcal{O}(n)$", "Typical usage"],
             ["Worst Case", r"$\\mathcal{O}(n)$", "Edge cases"]],
            row_labels=[Text("Type")],
            col_labels=[Text("Scenario"), Text("Time"), Text("Notes")],
            include_outer_lines=True,
            line_config={{"color": BLUE}}
        ).scale(0.6)
        
        table.next_to(applications_title, DOWN)
        
        # Professional fade in animation
        self.play(
            FadeIn(applications_title),
            Create(table)
        )
        self.wait(2)
        
        # Clean finish
        self.play(
            FadeOut(applications_title),
            Uncreate(table)
        )

if __name__ == "__main__":
    with tempconfig({{"format": "mp4", "pixel_width": 1280, "pixel_height": 720}}):
        scene = {class_name}Scene()
        scene.render()
'''
    
    # Write script to file
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{filename}.py")
    with open(script_path, "w") as f:
        f.write(script)
    
    return filename, script_path

def wait_for_video_completion(media_dir: str, class_name: str, max_wait: int = 300) -> bool:
    """Wait for all partial movie files to be generated.
    
    Args:
        media_dir: Path to media directory
        class_name: Name of the scene class
        max_wait: Maximum wait time in seconds
        
    Returns:
        bool: True if completed, False if timed out
    """
    start_time = time.time()
    partial_dir = None
    
    # Find the partial_movie_files directory
    while time.time() - start_time < max_wait:
        for root, dirs, files in os.walk(media_dir):
            if "partial_movie_files" in dirs:
                partial_dir = os.path.join(root, "partial_movie_files", class_name)
                if os.path.exists(partial_dir):
                    break
        if partial_dir:
            break
        time.sleep(1)
    
    if not partial_dir:
        return False

    # Count files with .mp4 extension
    total_files = 0
    generated_files = 0
    
    while time.time() - start_time < max_wait:
        mp4_files = [f for f in os.listdir(partial_dir) if f.endswith('.mp4')]
        current_count = len(mp4_files)
        
        if current_count > total_files:
            total_files = current_count
            generated_files = current_count
            continue
        
        if current_count == total_files and total_files > 0:
            # If count hasn't changed for 5 seconds, assume complete
            time.sleep(5)
            if len([f for f in os.listdir(partial_dir) if f.endswith('.mp4')]) == total_files:
                return True
        
        time.sleep(1)
    
    return False

def generate_animation_async(topic, request_id):
    try:
        # Emit initial progress - Script Generation
        socketio.emit('progress', {'progress': 10, 'request_id': request_id})
        
        # Generate the animation script
        filename, script_path = generate_manim_script(topic)
        
        # Emit progress - Script Generated
        socketio.emit('progress', {'progress': 30, 'request_id': request_id})
        
        # Generate the video using manim
        class_name = "".join(word.capitalize() for word in topic.split()) + "Scene"
        cmd = f"manim -pqm {script_path} {class_name}"
        
        socketio.emit('progress', {'progress': 50, 'request_id': request_id})
        
        # Start manim process
        process = subprocess.Popen(cmd, shell=True)
        
        # Wait for media directory
        media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "videos")
        
        # Monitor video generation
        if not wait_for_video_completion(media_dir, class_name):
            raise Exception("Video generation timed out")
        
        # Wait for process to complete
        process.wait()
        
        if process.returncode != 0:
            raise Exception("Video generation failed")
            
        socketio.emit('progress', {'progress': 80, 'request_id': request_id})
        
        # Move video to static directory
        video_filename = f"{topic.lower().replace(' ', '_')}.mp4"
        video_path = os.path.join(STATIC_VIDEO_DIR, video_filename)
        
        # Find the generated video file
        media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "videos")
        generated_video = None
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                if file.endswith(".mp4") and filename in root:
                    generated_video = os.path.join(root, file)
                    break
            if generated_video:
                break
        
        if generated_video:
            shutil.copy2(generated_video, video_path)
            
            # Clean up temporary files
            if os.path.exists(script_path):
                os.remove(script_path)
            
            video_url = f'http://127.0.0.1:5000/static/videos/{video_filename}'
            
            # Emit completion with video URL
            socketio.emit('completed', {
                'videoUrl': video_url,
                'topic': topic,
                'request_id': request_id
            })
        else:
            raise Exception("Failed to find generated video file")
            
    except Exception as e:
        logger.error(f"Error generating animation: {str(e)}")
        socketio.emit('error', {
            'message': str(e),
            'request_id': request_id
        })

@app.route('/visualize', methods=['POST', 'OPTIONS'])
def visualize():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        data = request.get_json()
        topic = data.get('topic')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
            
        # Generate a unique ID for this request
        request_id = str(uuid.uuid4())
        
        # Start animation generation in a background thread
        socketio.start_background_task(generate_animation_async, topic, request_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Animation generation started for topic "{topic}"',
            'request_id': request_id
        })
            
    except Exception as e:
        logger.error(f"Error in /visualize: {str(e)}")
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    logger.info(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f"Client disconnected: {request.sid}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Static directories
STATIC_VIDEO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "videos")
if not os.path.exists(STATIC_VIDEO_DIR):
    os.makedirs(STATIC_VIDEO_DIR)

@app.route('/static/videos/<path:filename>')
def serve_video(filename):
    response = send_from_directory(STATIC_VIDEO_DIR, filename)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'video/mp4'
    return response

@app.route('/test')
def test_page():
    return send_from_directory('.', 'test.html')

if __name__ == "__main__":
    socketio.run(app, 
        debug=True, 
        host="0.0.0.0", 
        port=5000,
        allow_unsafe_werkzeug=True
    )
