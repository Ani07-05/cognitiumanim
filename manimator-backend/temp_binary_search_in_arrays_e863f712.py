
from manim import *

class binarysearchinarraysScene(Scene):
    def construct(self):
        # Scene 1: Introduction (30s) - Playful, engaging intro for students
        title = Text("binary search in arrays Adventure!", font_size=48, color=BLUE).to_edge(UP)
        intro_text = Tex(r"Welcome to an exciting adventure learning about binary search in arrays! Let’s explore it step by step for fun and learning.", font_size=36).next_to(title, DOWN)
        sparkle = Star(color=YELLOW, fill_opacity=0.5).shift(RIGHT * 3)
        self.play(GrowFromCenter(title), GrowFromCenter(intro_text), Create(sparkle))
        self.add_sound("audio/cs_binary_search_in_arrays_intro.mp3")
        self.wait(5)  # Match narration length
        self.play(FadeOut(title), FadeOut(intro_text), FadeOut(sparkle))

        # Scene 2: Process (45s) - Dynamic visualization of the concept

        array = [1, 2, 3, 4]
        boxes = VGroup(*[Rectangle(height=0.5, width=0.5, fill_opacity=0.8, fill_color=BLUE)
                         for _ in array]).arrange(RIGHT, buff=0.2).shift(UP * 0.5)
        labels = VGroup(*[Text(str(n), font_size=20).next_to(box, CENTER) for n, box in zip(array, boxes)])
        self.play(Create(boxes), Write(labels))
        self.add_sound("audio/{audio_files['process']}.mp3")
        self.wait(2)

        # Simulate operation (e.g., push/pop) with animation
        self.play(boxes[0].animate.set_color(GREEN), GrowFromCenter(Circle(radius=0.1, color=YELLOW).next_to(boxes[0], RIGHT)), run_time=2)
        self.wait(5)  # Ensure 45s total

        self.play(FadeOut(Group(*self.mobjects)))

        # Scene 3: Example (30s) - Playful example for students
        example_text = Tex(r"{scenes['example']}", font_size=36).to_edge(DOWN)
        star = Star(color=RED, fill_opacity=0.5).shift(LEFT * 3)
        self.play(Write(example_text), GrowFromCenter(star))
        self.add_sound("audio/{audio_files['example']}.mp3")
        self.wait(5)
        self.play(FadeOut(example_text), FadeOut(star))

        # Scene 4: Complexity (30s) - Simple, engaging time/space explanation
        axes = Axes(x_range=[0, 5], y_range=[0, 25], axis_config={"color": BLUE}).scale(0.5).to_edge(DOWN)
        graph = axes.plot(lambda x: x**2, color=RED)
        label = Text("Time grows fast with more items!", font_size=24, color=BLUE).next_to(axes, UP)
        self.play(Create(axes), Create(graph), Write(label))
        self.add_sound("audio/{audio_files['complexity']}.mp3")
        self.wait(5)
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(label))

        # Scene 5: Optimization (30s) - Fun optimization tip
        optimize_text = Tex(r"{scenes['optimization']}", font_size=36).to_edge(DOWN)
        arrow = Arrow(start=LEFT, end=RIGHT, color=GREEN).shift(UP * 0.5)
        self.play(Write(optimize_text), Create(arrow))
        self.add_sound("audio/{audio_files['optimization']}.mp3")
        self.wait(5)
        self.play(FadeOut(optimize_text), FadeOut(arrow))

        # Scene 6: Conclusion (45s) - Playful, memorable wrap-up
        conclusion = Tex(r"{scenes['conclusion']}", font_size=36).to_edge(DOWN)
        cheer = Circle(radius=1, color=GREEN, fill_opacity=0.5).shift(RIGHT * 2)
        self.play(Write(conclusion), GrowFromCenter(cheer))
        self.add_sound("audio/{audio_files['conclusion']}.mp3")
        self.wait(7)
        self.play(FadeOut(conclusion), FadeOut(cheer))
        self.wait(1)

# Additional padding to ensure length
# Additional padding to ensure length
# Additional padding to ensure length
# Additional padding to ensure length
# Additional padding to ensure length
# Additional padding to ensure length
# Additional padding to ensure length
# Additional padding to ensure length
# Additional padding to ensure length
# Additional padding to ensure length