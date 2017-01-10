from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.fractals import *
from topics.number_line import *
from topics.combinatorics import *
from topics.numerals import *
from topics.three_dimensions import *
from topics.objects import *
from scene import Scene
from scene.zoomed_scene import ZoomedScene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

from eoc.chapter1 import OpeningQuote
from eoc.graph_scene import *

DISTANCE_COLOR = BLUE
TIME_COLOR = YELLOW
VELOCITY_COLOR = GREEN

class Car(SVGMobject):
    CONFIG = {
        "file_name" : "Car", 
        "height" : 1,
        "color" : "#BBBBBB",
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.scale_to_fit_height(self.height)
        self.set_stroke(color = WHITE, width = 0)
        self.set_fill(self.color, opacity = 1)

        randy = Randolph(mode = "happy")
        randy.scale_to_fit_height(0.6*self.get_height())
        randy.stretch(0.8, 0)
        randy.look(RIGHT)
        randy.move_to(self)
        randy.shift(0.07*self.height*(RIGHT+UP))
        self.add_to_back(randy)

        orientation_line = Line(self.get_left(), self.get_right())
        orientation_line.set_stroke(width = 0)
        self.add(orientation_line)
        self.orientation_line = orientation_line


        self.add_treds_to_tires()

    def move_to(self, point_or_mobject):
        vect = rotate_vector(
            UP+LEFT, self.orientation_line.get_angle()
        )
        self.next_to(point_or_mobject, vect, buff = 0)
        return self

    def get_front_line(self):
        return DashedLine(
            self.get_corner(UP+RIGHT), 
            self.get_corner(DOWN+RIGHT),
            color = DISTANCE_COLOR,
            dashed_segment_length = 0.05,
        )

    def add_treds_to_tires(self):
        for tire in self.get_tires():
            radius = tire.get_width()/2
            center = tire.get_center()
            tred = Line(
                0.9*radius*RIGHT, 1.4*radius*RIGHT,
                stroke_width = 2,
                color = BLACK
            )
            tred.rotate_in_place(np.pi/4)
            for theta in np.arange(0, 2*np.pi, np.pi/4):
                new_tred = tred.copy()
                new_tred.rotate(theta)
                new_tred.shift(center)
                tire.add(new_tred)
        return self

    def get_tires(self):
        return VGroup(self[1][1], self[1][3])

class MoveCar(ApplyMethod):
    def __init__(self, car, target_point, **kwargs):
        ApplyMethod.__init__(self, car.move_to, target_point, **kwargs)
        displacement = self.ending_mobject.get_right()-self.starting_mobject.get_right()
        distance = np.linalg.norm(displacement)
        tire_radius = car.get_tires()[0].get_width()/2
        self.total_tire_radians = -distance/tire_radius

    def update_mobject(self, alpha):
        ApplyMethod.update_mobject(self, alpha)
        if alpha == 0:
            return
        radians = alpha*self.total_tire_radians
        for tire in self.mobject.get_tires():
            tire.rotate_in_place(radians)

class IncrementNumber(Succession):
    CONFIG = {
        "start_num" : 0,
        "changes_per_second" : 1,
        "run_time" : 11,
    }
    def __init__(self, num_mob, **kwargs):
        digest_config(self, kwargs)
        n_iterations = int(self.run_time * self.changes_per_second)
        new_num_mobs = [
            TexMobject(str(num)).move_to(num_mob, LEFT)
            for num in range(self.start_num, self.start_num+n_iterations)
        ]
        transforms = [
            Transform(
                num_mob, new_num_mob, 
                run_time = 1.0/self.changes_per_second,
                rate_func = squish_rate_func(smooth, 0, 0.5)
            )
            for new_num_mob in new_num_mobs
        ]
        Succession.__init__(
            self, *transforms, **{
                "rate_func" : None,
                "run_time" : self.run_time,
            }
        )

class IncrementTest(Scene):
    def construct(self):
        num = TexMobject("0")
        num.shift(UP)
        self.play(IncrementNumber(num))
        self.dither()



############################

class Chapter2OpeningQuote(OpeningQuote):
    CONFIG = {
        "quote" : [
            "So far as the theories of mathematics are about",
            "reality,", 
            "they are not",
            "certain;", 
            "so far as they are",
            "certain,", 
            "they are not about",
            "reality.",
        ],
        "highlighted_quote_terms" : {
            "reality," : BLUE,
            "certain;" : GREEN,
            "certain," : GREEN,
            "reality." : BLUE,
        },
        "author" : "Albert Einstein"
    }

class Introduction(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "What is a derivative?"
        )
        self.play(self.get_teacher().change_mode, "happy")
        self.dither()
        self.teacher_says(
            "It's actually a \\\\",
            "very subtle idea",
            target_mode = "well"
        )
        self.change_student_modes(None, "pondering", "thinking")
        self.dither()
        self.change_student_modes("erm")
        self.student_says(
            "Doesn't the derivative measure\\\\",
            "instantaneous rate of change", "?",
            student_index = 0,
        )
        self.dither()

        bubble = self.get_students()[0].bubble
        phrase = bubble.content[1]
        bubble.content.remove(phrase)
        self.play(
            phrase.center,
            phrase.scale, 1.5,
            phrase.to_edge, UP,
            FadeOut(bubble),
            FadeOut(bubble.content),
            *it.chain(*[
                [
                    pi.change_mode, mode,
                    pi.look_at, SPACE_HEIGHT*UP
                ]
                for pi, mode in zip(self.get_everyone(), [
                    "speaking", "pondering", "confused", "confused",
                ])
            ])
        )
        self.dither()
        change = VGroup(*phrase[-len("change"):])
        instantaneous = VGroup(*phrase[:len("instantaneous")])
        change_brace = Brace(change)
        change_description = change_brace.get_text(
            "Requires multiple \\\\ points in time"
        )
        instantaneous_brace = Brace(instantaneous)
        instantaneous_description = instantaneous_brace.get_text(
            "One point \\\\ in time"
        )
        clock = Clock()
        clock.next_to(change_description, DOWN)
        def get_clock_anim(run_time = 3):
            return ClockPassesTime(
                clock,
                hours_passed = 0.4*run_time,
                run_time = run_time,
            )
        self.play(FadeIn(clock))
        self.play(
            change.gradient_highlight, BLUE, YELLOW,
            GrowFromCenter(change_brace),
            Write(change_description),
            get_clock_anim()
        )
        self.play(get_clock_anim(1))
        stopped_clock = clock.copy()
        stopped_clock.next_to(instantaneous_description, DOWN)
        self.play(
            instantaneous.highlight, BLUE,
            GrowFromCenter(instantaneous_brace),
            Transform(change_description.copy(), instantaneous_description),
            clock.copy().next_to, instantaneous_description, DOWN,
            get_clock_anim(3)
        )
        self.play(get_clock_anim(6))

class FathersOfCalculus(Scene):
    CONFIG = {
        "names" : [
            "Barrow",
            "Newton", 
            "Leibniz",
            "Cauchy",
            "Weierstrass",
        ],
        "picture_height" : 2.5,
    }
    def construct(self):
        title = TextMobject("(A few) Fathers of Calculus")
        title.to_edge(UP)
        self.add(title)

        men = Mobject()
        for name in self.names:
            image = ImageMobject(name, invert = False)
            image.scale_to_fit_height(self.picture_height)
            title = TextMobject(name)
            title.scale(0.8)
            title.next_to(image, DOWN)
            image.add(title)
            men.add(image)
        men.arrange_submobjects(RIGHT, aligned_edge = UP)
        men.shift(DOWN)

        discover_brace = Brace(Mobject(*men[:3]), UP)
        discover = discover_brace.get_text("Discovered it")
        VGroup(discover_brace, discover).highlight(BLUE)
        rigor_brace = Brace(Mobject(*men[3:]), UP)
        rigor = rigor_brace.get_text("Made it rigorous")
        rigor.shift(0.1*DOWN)
        VGroup(rigor_brace, rigor).highlight(YELLOW)


        for man in men:
            self.play(FadeIn(man))
        self.play(
            GrowFromCenter(discover_brace),
            Write(discover, run_time = 1)
        )
        self.play(
            GrowFromCenter(rigor_brace),
            Write(rigor, run_time = 1)
        )
        self.dither()

class IntroduceCar(Scene):
    CONFIG = {
        "should_transition_to_graph" : True,
        "show_distance" : True,
    }
    def construct(self):
        point_A = DOWN+4*LEFT
        point_B = DOWN+5*RIGHT
        A = Dot(point_A)
        B = Dot(point_B)
        line = Line(point_A, point_B)
        VGroup(A, B, line).highlight(WHITE)        
        for dot, tex in (A, "A"), (B, "B"):
            label = TexMobject(tex).next_to(dot, DOWN)
            dot.add(label)

        car = Car()
        self.car = car #For introduce_added_mobjects use in subclasses
        car.move_to(point_A)
        front_line = car.get_front_line()

        time_label = TextMobject("Time (in seconds):", "0")
        time_label.shift(2*UP)

        distance_brace = Brace(line, UP)
        # distance_brace.set_fill(opacity = 0.5)
        distance = distance_brace.get_text("100m")

        self.add(A, B, line, car, time_label)
        self.play(ShowCreation(front_line))
        self.play(FadeOut(front_line))
        self.introduce_added_mobjects()
        self.play(
            MoveCar(car, point_B, run_time = 10),
            IncrementNumber(time_label[1], run_time = 11),
            *self.get_added_movement_anims()
        )
        front_line = car.get_front_line()
        self.play(ShowCreation(front_line))
        self.play(FadeOut(front_line))

        if self.show_distance:
            self.play(
                GrowFromCenter(distance_brace),
                Write(distance)
            )
            self.dither()

        if self.should_transition_to_graph:
            self.play(
                car.move_to, point_A,
                FadeOut(time_label),
                FadeOut(distance_brace),
                FadeOut(distance),
            )
            graph_scene = GraphCarTrajectory(skip_animations = True)
            origin = graph_scene.graph_origin
            top = graph_scene.coords_to_point(0, 100)
            new_length = np.linalg.norm(top-origin)
            new_point_B = point_A + new_length*RIGHT
            car_line_group = VGroup(car, A, B, line)
            for mob in car_line_group:
                mob.generate_target()
            car_line_group.target = VGroup(*[
                m.target for m in car_line_group
            ])
            B = car_line_group[2]
            B.target.shift(new_point_B - point_B)
            line.target.put_start_and_end_on(
                point_A, new_point_B
            )

            car_line_group.target.rotate(np.pi/2, about_point = point_A)
            car_line_group.target.shift(graph_scene.graph_origin - point_A)
            self.play(MoveToTarget(car_line_group, path_arc = np.pi/2))
            self.dither()

    def introduce_added_mobjects(self):
        pass

    def get_added_movement_anims(self):
        return []

class GraphCarTrajectory(GraphScene):
    CONFIG = {
        "x_min" : 0,
        "x_max" : 10.01,
        "x_labeled_nums" : range(1, 11),
        "x_axis_label" : "Time (seconds)",
        "y_min" : 0,
        "y_max" : 110,
        "y_tick_frequency" : 10,
        "y_labeled_nums" : range(10, 110, 10),
        "y_axis_label" : "Distance traveled \\\\ (meters)",
        "graph_origin" : 2.5*DOWN + 5*LEFT,
        "default_graph_colors" : [DISTANCE_COLOR, VELOCITY_COLOR],
        "default_derivative_color" : VELOCITY_COLOR,
    }
    def construct(self):
        self.setup_axes(animate = False)
        graph = self.graph_sigmoid_trajectory_function()
        origin = self.coords_to_point(0, 0)

        self.introduce_graph(graph, origin)
        self.comment_on_slope(graph, origin)
        self.show_velocity_graph()
        self.ask_critically_about_velocity()

    def graph_sigmoid_trajectory_function(self, **kwargs):
        graph = self.graph_function(
            lambda t : 100*smooth(t/10.),
            **kwargs
        )
        return graph

    def introduce_graph(self, graph, origin):
        h_line, v_line = [
            Line(origin, origin, color = color, stroke_width = 2)
            for color in TIME_COLOR, DISTANCE_COLOR
        ]
        def h_update(h_line, proportion = 1):
            end = graph.point_from_proportion(proportion)
            t_axis_point = end[0]*RIGHT + origin[1]*UP
            h_line.put_start_and_end_on(t_axis_point, end)
        def v_update(v_line, proportion = 1):
            end = graph.point_from_proportion(proportion)
            d_axis_point = origin[0]*RIGHT + end[1]*UP
            v_line.put_start_and_end_on(d_axis_point, end)

        car = Car()
        car.rotate(np.pi/2)
        car.move_to(origin)
        self.add(car)
        self.play(
            ShowCreation(
                graph,
                rate_func = None,
            ),
            MoveCar(
                car, self.coords_to_point(0, 100),
            ),
            UpdateFromFunc(h_line, h_update),
            UpdateFromFunc(v_line, v_update),
            run_time = 10,
        )
        self.dither()
        self.play(*map(FadeOut, [h_line, v_line, car]))

        #Show example vertical distance
        h_update(h_line, 0.6)
        t_dot = Dot(h_line.get_start(), color = h_line.get_color())
        t_dot.save_state()
        t_dot.move_to(self.x_axis_label_mob)
        t_dot.set_fill(opacity = 0)
        dashed_h = DashedLine(*h_line.get_start_and_end())
        dashed_h.highlight(h_line.get_color())
        brace = Brace(dashed_h, RIGHT)
        brace_text = brace.get_text("Distance traveled")
        self.play(t_dot.restore)
        self.dither()
        self.play(ShowCreation(dashed_h))
        self.play(
            GrowFromCenter(brace),
            Write(brace_text)
        )
        self.dither(2)
        self.play(*map(FadeOut, [t_dot, dashed_h, brace, brace_text]))

        #Name graph
        s_of_t = TexMobject("s(t)")
        s_of_t.next_to(
            graph.point_from_proportion(1), 
            DOWN+RIGHT,
            buff = SMALL_BUFF
        )
        s = s_of_t[0]
        d = TexMobject("d")
        d.move_to(s, DOWN)
        d.highlight(DISTANCE_COLOR)

        self.play(Write(s_of_t))
        self.dither()
        s.save_state()
        self.play(Transform(s, d))
        self.dither()
        self.play(s.restore)

    def comment_on_slope(self, graph, origin):
        delta_t = 1
        curr_time = 0
        ghost_line = Line(
            origin, 
            self.coords_to_point(delta_t, self.y_max)
        )
        rect = Rectangle().replace(ghost_line, stretch = True)
        rect.set_stroke(width = 0)
        rect.set_fill(TIME_COLOR, opacity = 0.3)

        change_lines = self.get_change_lines(curr_time, delta_t)
        self.play(FadeIn(rect))
        self.dither()
        self.play(Write(change_lines))
        self.dither()
        for x in range(1, 10):
            curr_time = x
            new_change_lines = self.get_change_lines(curr_time, delta_t)
            self.play(
                rect.move_to, self.coords_to_point(curr_time, 0), DOWN+LEFT,
                Transform(change_lines, new_change_lines)
            )
            if curr_time == 5:
                text = change_lines[-1].get_text(
                    "$\\frac{\\text{meters}}{\\text{second}}$"
                )
                self.play(Write(text))
                self.dither()
                self.play(FadeOut(text))
            else:
                self.dither()
        self.play(*map(FadeOut, [rect, change_lines]))
        self.rect = rect

    def get_change_lines(self, curr_time, delta_t = 1):
        p1 = self.input_to_graph_point(curr_time)
        p2 = self.input_to_graph_point(curr_time+delta_t)
        interim_point = p2[0]*RIGHT + p1[1]*UP
        delta_t_line = Line(p1, interim_point, color = TIME_COLOR)
        delta_s_line = Line(interim_point, p2, color = DISTANCE_COLOR)
        brace = Brace(delta_s_line, RIGHT, buff = SMALL_BUFF)
        return VGroup(delta_t_line, delta_s_line, brace)

    def show_velocity_graph(self):
        velocity_graph = self.get_derivative_graph()

        self.play(ShowCreation(velocity_graph))
        def get_velocity_label(v_graph):
            result = self.label_graph(
                v_graph,
                label = "v(t)",
                direction = UP+RIGHT,
                proportion = 0.5,
                buff = SMALL_BUFF,
                animate = False,
            )
            self.remove(result)
            return result
        label = get_velocity_label(velocity_graph)
        self.play(Write(label))
        self.dither()
        self.rect.move_to(self.coords_to_point(0, 0), DOWN+LEFT)
        self.play(FadeIn(self.rect))
        self.dither()
        for time, show_slope in (4.5, True), (9, False):
            self.play(
                self.rect.move_to, self.coords_to_point(time, 0), DOWN+LEFT
            )
            if show_slope:
                change_lines = self.get_change_lines(time)
                self.play(FadeIn(change_lines))
                self.dither()
                self.play(FadeOut(change_lines))
            else:
                self.dither()
        self.play(FadeOut(self.rect))

        #Change distance and velocity graphs
        self.graph.save_state()
        velocity_graph.save_state()
        label.save_state()
        def shallow_slope(t):
            return 100*smooth(t/10., inflection = 4)
        def steep_slope(t):
            return 100*smooth(t/10., inflection = 25)
        def double_smooth_graph_function(t):
            if t < 5:
                return 50*smooth(t/5.)
            else:
                return 50*(1+smooth((t-5)/5.))
        graph_funcs = [
            shallow_slope,
            steep_slope,
            double_smooth_graph_function,
        ]
        for graph_func in graph_funcs:
            new_graph = self.graph_function(
                graph_func,
                is_main_graph = False
            )
            self.remove(new_graph)
            new_velocity_graph = self.get_derivative_graph(
                graph = new_graph,
            )
            new_velocity_label = get_velocity_label(new_velocity_graph)

            self.play(Transform(self.graph, new_graph))
            self.play(
                Transform(velocity_graph, new_velocity_graph),
                Transform(label, new_velocity_label),
            )
            self.dither(2)
        self.play(self.graph.restore)
        self.play(
            velocity_graph.restore,
            label.restore,
        )
        self.dither(2)

    def ask_critically_about_velocity(self):
        morty = Mortimer().flip()
        morty.to_corner(DOWN+LEFT)
        self.play(PiCreatureSays(morty,
            "Think critically about \\\\",
            "what velocity means."
        ))
        self.play(Blink(morty))
        self.dither()

class ShowSpeedometer(IntroduceCar):
    CONFIG = {
        "num_ticks" : 8,
        "tick_length" : 0.2,
        "needle_width" : 0.1,
        "needle_height" : 0.8,
        "should_transition_to_graph" : False,
        "show_distance" : False,
    }
    def setup(self):
        start_angle = -np.pi/6
        end_angle = 7*np.pi/6
        speedomoeter = Arc(
            start_angle = start_angle,
            angle = end_angle-start_angle
        )
        tick_angle_range = np.linspace(end_angle, start_angle, self.num_ticks)
        for index, angle in enumerate(tick_angle_range):
            vect = rotate_vector(RIGHT, angle)
            tick = Line((1-self.tick_length)*vect, vect)
            label = TexMobject(str(10*index))
            label.scale_to_fit_height(self.tick_length)
            label.shift((1+self.tick_length)*vect)
            speedomoeter.add(tick, label)

        needle = Polygon(
            LEFT, UP, RIGHT,
            stroke_width = 0,
            fill_opacity = 1,
            fill_color = YELLOW
        )
        needle.stretch_to_fit_width(self.needle_width)
        needle.stretch_to_fit_height(self.needle_height)
        needle.rotate(end_angle-np.pi/2)
        speedomoeter.add(needle)
        speedomoeter.needle = needle

        speedomoeter.center_offset = speedomoeter.get_center()

        speedomoeter_title = TextMobject("Speedometer")
        speedomoeter_title.to_corner(UP+LEFT)
        speedomoeter.next_to(speedomoeter_title, DOWN)

        self.speedomoeter = speedomoeter
        self.speedomoeter_title = speedomoeter_title

    def introduce_added_mobjects(self):
        speedomoeter = self.speedomoeter
        speedomoeter_title = self.speedomoeter_title

        speedomoeter.save_state()
        speedomoeter.rotate(-np.pi/2, UP)
        speedomoeter.scale_to_fit_height(self.car.get_height()/4)
        speedomoeter.move_to(self.car)
        speedomoeter.shift((self.car.get_width()/4)*RIGHT)

        self.play(speedomoeter.restore, run_time = 2)
        self.play(Write(speedomoeter_title, run_time = 1))

    def get_added_movement_anims(self):
        needle = self.speedomoeter.needle
        center = self.speedomoeter.get_center() - self.speedomoeter.center_offset
        return [
            Rotating(
                needle, 
                about_point = center,
                radians = -np.pi/2,
                run_time = 10,
                rate_func = there_and_back
            )
        ]

    # def construct(self):
    #     self.add(self.speedomoeter)
    #     self.play(*self.get_added_movement_anims())

class VelocityInAMomentMakesNoSense(Scene):
    def construct(self):
        randy = Randolph()
        randy.next_to(ORIGIN, DOWN+LEFT)
        words = TextMobject("Velocity in \\\\ a moment")
        words.next_to(randy, UP+RIGHT)
        randy.look_at(words)
        q_marks = TextMobject("???")
        q_marks.next_to(randy, UP)

        self.play(
            randy.change_mode, "confused",
            Write(words)
        )
        self.play(Blink(randy))
        self.play(Write(q_marks))
        self.play(Blink(randy))
        self.dither()

class SnapshotOfACar(Scene):
    def construct(self):
        car = Car()
        car.scale(1.5)
        car.move_to(3*LEFT+DOWN)
        flash_box = Rectangle(
            width = 2*SPACE_WIDTH,
            height = 2*SPACE_HEIGHT,
            stroke_width = 0,
            fill_color = WHITE,
            fill_opacity = 1,
        )
        speed_lines = VGroup(*[
            Line(point, point+0.5*LEFT)
            for point in [
                0.5*UP+0.25*RIGHT,
                ORIGIN, 
                0.5*DOWN+0.25*RIGHT
            ]
        ])
        question = TextMobject("""
            How fast is
            this car going?
        """)

        self.play(MoveCar(
            car, RIGHT+DOWN, 
            run_time = 2,
            rate_func = rush_into
        ))
        car.get_tires().highlight(GREY)
        speed_lines.next_to(car, LEFT)
        self.add(speed_lines)
        self.play(
            flash_box.set_fill, None, 0,
            rate_func = rush_from
        )
        question.next_to(car, UP, buff = LARGE_BUFF)
        self.play(Write(question, run_time = 2))
        self.dither(2)

class CompareTwoTimes(Scene):
    CONFIG = {
        "start_distance" : 30,
        "start_time" : 4,
        "end_distance" : 50,
        "end_time" : 5,
        "fade_at_the_end" : True,
    }
    def construct(self):
        self.introduce_states()
        self.show_equation()
        if self.fade_at_the_end:
            self.fade_all_but_one_moment()

    def introduce_states(self):
        state1 = self.get_car_state(self.start_distance, self.start_time)
        state2 = self.get_car_state(self.end_distance, self.end_time)

        state1.to_corner(UP+LEFT)
        state2.to_corner(DOWN+LEFT)

        dividers = VGroup(
            Line(SPACE_WIDTH*LEFT, RIGHT),
            Line(RIGHT+SPACE_HEIGHT*UP, RIGHT+SPACE_HEIGHT*DOWN),
        )
        dividers.highlight(GREY)

        self.add(dividers, state1)
        self.dither()
        copied_state = state1.copy()
        self.play(copied_state.move_to, state2)
        self.play(Transform(copied_state, state2))
        self.dither(2)
        self.keeper = state1

    def show_equation(self):
        velocity = TextMobject("Velocity")
        change_over_change = TexMobject(
            "\\frac{\\text{Change in distance}}{\\text{Change in time}}"
        )
        formula = TexMobject(
            "\\frac{(%s - %s) \\text{ meters}}{(%s - %s) \\text{ seconds}}"%(
                str(self.end_distance), str(self.start_distance),
                str(self.end_time), str(self.start_time),
            )
        )
        ed_len = len(str(self.end_distance))
        sd_len = len(str(self.start_distance))
        et_len = len(str(self.end_time))
        st_len = len(str(self.start_time))
        seconds_len = len("seconds")
        VGroup(
            VGroup(*formula[1:1+ed_len]),
            VGroup(*formula[2+ed_len:2+ed_len+sd_len])
        ).highlight(DISTANCE_COLOR)
        VGroup(
            VGroup(*formula[-2-seconds_len-et_len-st_len:-2-seconds_len-st_len]),
            VGroup(*formula[-1-seconds_len-st_len:-1-seconds_len]),
        ).highlight(TIME_COLOR)

        down_arrow1 = TexMobject("\\Downarrow")
        down_arrow2 = TexMobject("\\Downarrow")
        group = VGroup(
            velocity, down_arrow1, 
            change_over_change, down_arrow2,
            formula,
        )
        group.arrange_submobjects(DOWN)
        group.to_corner(UP+RIGHT)

        self.play(FadeIn(
            group, submobject_mode = "lagged_start",
            run_time = 3
        ))
        self.dither(3)
        self.formula = formula

    def fade_all_but_one_moment(self):
        anims = [
            ApplyMethod(mob.fade, 0.5)
            for mob in self.get_mobjects()
        ]
        anims.append(Animation(self.keeper.copy()))
        self.play(*anims)
        self.dither()

    def get_car_state(self, distance, time):
        line = Line(3*LEFT, 3*RIGHT)
        dots = map(Dot, line.get_start_and_end())
        line.add(*dots)
        car = Car()
        car.move_to(line.get_start())
        car.shift((distance/10)*RIGHT)
        front_line = car.get_front_line()

        brace = Brace(VGroup(dots[0], front_line), DOWN)
        distance_label = brace.get_text(
            str(distance), " meters"
        )
        distance_label.highlight_by_tex(str(distance), DISTANCE_COLOR)
        brace.add(distance_label)
        time_label = TextMobject(
            "Time:", str(time), "seconds"
        )
        time_label.highlight_by_tex(str(time), TIME_COLOR)
        time_label.next_to(
            VGroup(line, car), UP,
            aligned_edge = LEFT
        )

        return VGroup(line, car, front_line, brace, time_label)

class VelocityAtIndividualPointsVsPairs(GraphCarTrajectory):
    CONFIG = {
        "start_time" : 6.5,
        "end_time" : 3,
        "dt" : 1.0,
    }
    def construct(self):
        self.setup_axes(animate = False)
        distance_graph = self.graph_function(lambda t : 100*smooth(t/10.))
        distance_label = self.label_graph(
            distance_graph,
            label = "s(t)",
            proportion = 1,
            direction = RIGHT,
            buff = SMALL_BUFF
        )
        velocity_graph = self.get_derivative_graph()
        self.play(ShowCreation(velocity_graph))
        velocity_label = self.label_graph(
            velocity_graph, 
            label = "v(t)",
            proportion = self.start_time/10.0, 
            direction = UP,
            buff = MED_BUFF
        )
        velocity_graph.add(velocity_label)

        self.show_individual_times_to_velocity(velocity_graph)
        self.play(velocity_graph.fade, 0.4)
        self.show_two_times_on_distance()
        self.show_confused_pi_creature()

    def show_individual_times_to_velocity(self, velocity_graph):
        start_time = self.start_time
        end_time = self.end_time
        line = self.get_vertical_line_to_graph(start_time, velocity_graph)
        def line_update(line, alpha):
            time = interpolate(start_time, end_time, alpha)
            line.put_start_and_end_on(
                self.coords_to_point(time, 0),
                self.input_to_graph_point(time, graph = velocity_graph)
            )

        self.play(ShowCreation(line))
        self.dither()
        self.play(UpdateFromAlphaFunc(
            line, line_update,
            run_time = 4,
            rate_func = there_and_back
        ))
        self.dither()
        velocity_graph.add(line)

    def show_two_times_on_distance(self):
        line1 = self.get_vertical_line_to_graph(self.start_time-self.dt/2.0)
        line2 = self.get_vertical_line_to_graph(self.start_time+self.dt/2.0)
        p1 = line1.get_end()
        p2 = line2.get_end()
        interim_point = p2[0]*RIGHT+p1[1]*UP
        dt_line = Line(p1, interim_point, color = TIME_COLOR)
        ds_line = Line(interim_point, p2, color = DISTANCE_COLOR)
        dt_brace = Brace(dt_line, DOWN, buff = SMALL_BUFF)
        ds_brace = Brace(ds_line, RIGHT, buff = SMALL_BUFF)
        dt_text = dt_brace.get_text("Change in time", buff = SMALL_BUFF)
        ds_text = ds_brace.get_text("Change in distance", buff = SMALL_BUFF)

        self.play(ShowCreation(VGroup(line1, line2)))
        for line, brace, text in (dt_line, dt_brace, dt_text), (ds_line, ds_brace, ds_text):
            brace.highlight(line.get_color())
            text.highlight(line.get_color())
            text.add_background_rectangle()
            self.play(
                ShowCreation(line),
                GrowFromCenter(brace),
                Write(text)
            )
            self.dither()

    def show_confused_pi_creature(self):
        randy = Randolph()
        randy.to_corner(DOWN+LEFT)
        randy.shift(2*RIGHT)

        self.play(randy.change_mode, "confused")
        self.play(Blink(randy))
        self.dither(2)
        self.play(Blink(randy))
        self.play(randy.change_mode, "erm")
        self.dither()
        self.play(Blink(randy))
        self.dither(2)

class CompareTwoVerySimilarTimes(CompareTwoTimes):
    CONFIG = {
        "start_distance" : 20,
        "start_time" : 3,
        "end_distance" : 20.21,
        "end_time" : 3.01,
        "fade_at_the_end" : False,
    }
    def construct(self):
        CompareTwoTimes.construct(self)

        formula = self.formula
        ds_symbols, dt_symbols = [
            VGroup(*[
                mob
                for mob in formula
                if mob.get_color() == Color(color)
            ])
            for color in DISTANCE_COLOR, TIME_COLOR
        ]
        ds_brace = Brace(ds_symbols, UP)
        ds_text = ds_brace.get_text("$ds$", buff = SMALL_BUFF)
        ds_text.highlight(DISTANCE_COLOR)
        dt_brace = Brace(dt_symbols, DOWN)
        dt_text = dt_brace.get_text("$dt$", buff = SMALL_BUFF)
        dt_text.highlight(TIME_COLOR)

        self.play(
            GrowFromCenter(dt_brace),
            Write(dt_text)
        )
        formula.add(dt_brace, dt_text)
        self.dither(2)

        formula.generate_target()
        VGroup(
            ds_brace, ds_text, formula.target
        ).move_to(formula, UP).shift(0.5*UP)
        self.play(
            MoveToTarget(formula),
            GrowFromCenter(ds_brace),
            Write(ds_text)
        )
        self.dither(2)

class DsOverDtGraphically(GraphCarTrajectory, ZoomedScene):
    CONFIG = {
        "dt" : 0.1,
        "zoom_factor" : 4,#Before being shrunk by dt
        "start_time" : 3,
        "end_time" : 7,
    }
    def construct(self):
        self.setup_axes(animate = False)
        distance_graph = self.graph_function(
            lambda t : 100*smooth(t/10.),
            animate = False,
        )
        distance_label = self.label_graph(
            distance_graph,
            label = "s(t)",
            proportion = 0.9,
            direction = UP+LEFT,
            buff = SMALL_BUFF
        )
        input_point_line = self.get_vertical_line_to_graph(
            self.start_time,
            line_kwargs = {
                "dashed_segment_length" : 0.02,
                "stroke_width" : 4,
                "color" : WHITE,
            },
        )
        def get_ds_dt_group(time):
            point1 = self.input_to_graph_point(time)
            point2 = self.input_to_graph_point(time+self.dt)
            interim_point = point2[0]*RIGHT+point1[1]*UP
            dt_line = Line(point1, interim_point, color = TIME_COLOR)
            ds_line = Line(interim_point, point2, color = DISTANCE_COLOR)
            result = VGroup()
            for line, char, vect in (dt_line, "t", DOWN), (ds_line, "s", RIGHT):
                line.scale(1./self.dt)
                brace = Brace(line, vect)
                text = brace.get_text("$d%s$"%char)
                text.next_to(brace, vect)
                text.highlight(line.get_color())
                subgroup = VGroup(line, brace, text)
                subgroup.scale(self.dt)
                result.add(subgroup)
            return result
        def align_little_rectangle_on_ds_dt_group(rect):
            rect.move_to(ds_dt_group, DOWN+RIGHT)
            rect.shift(self.dt*(DOWN+RIGHT)/4)
            return rect
        ds_dt_group = get_ds_dt_group(self.start_time)

        #Initially zoom in
        self.play(ShowCreation(input_point_line))
        self.activate_zooming()
        self.play(*map(FadeIn, [self.big_rectangle, self.little_rectangle]))
        self.play(
            ApplyFunction(
                align_little_rectangle_on_ds_dt_group,
                self.little_rectangle
            )
        )
        self.little_rectangle.generate_target()
        self.little_rectangle.target.scale(self.zoom_factor*self.dt)
        align_little_rectangle_on_ds_dt_group(
            self.little_rectangle.target
        )
        self.play(
            MoveToTarget(self.little_rectangle),
            run_time = 3
        )
        for subgroup in ds_dt_group:
            line, brace, text= subgroup
            self.play(ShowCreation(line))
            self.play(
                GrowFromCenter(brace),
                Write(text)
            )
            self.dither()

        #Show as function
        frac = TexMobject("\\frac{ds}{dt}")
        VGroup(*frac[:2]).highlight(DISTANCE_COLOR)
        VGroup(*frac[-2:]).highlight(TIME_COLOR)
        frac.next_to(self.input_to_graph_point(5.25), DOWN+RIGHT)
        rise_over_run = TexMobject(
            "=\\frac{\\text{rise}}{\\text{run}}"
        )
        rise_over_run.next_to(frac, RIGHT)
        of_t = TexMobject("(t)")
        of_t.next_to(frac, RIGHT, buff = SMALL_BUFF)

        dt_choice = TexMobject("dt = 0.01")
        dt_choice.highlight(TIME_COLOR)
        dt_choice.next_to(of_t, UP, aligned_edge = LEFT, buff = LARGE_BUFF)


        full_formula = TexMobject(
            "=\\frac{s(t+dt) - s(t)}{dt}"
        )
        full_formula.next_to(of_t)
        s_t_plus_dt = VGroup(*full_formula[1:8])
        s_t = VGroup(*full_formula[9:13])
        numerator = VGroup(*full_formula[1:13])
        lower_dt =  VGroup(*full_formula[-2:])
        upper_dt = VGroup(*full_formula[5:7])
        equals = full_formula[0]
        frac_line = full_formula[-3]
        s_t_plus_dt.highlight(DISTANCE_COLOR)
        s_t.highlight(DISTANCE_COLOR)
        lower_dt.highlight(TIME_COLOR)
        upper_dt.highlight(TIME_COLOR)

        velocity_graph = self.get_derivative_graph()
        t_tick_marks = VGroup(*[
            Line(
                UP, DOWN,
                color = TIME_COLOR,
                stroke_width = 3,
            ).scale(0.1).move_to(self.coords_to_point(t, 0))
            for t in np.linspace(0, 10, 75)
        ])

        v_line_at_t, v_line_at_t_plus_dt = [
            self.get_vertical_line_to_graph(
                time,
                line_class = Line,
                line_kwargs = {"color" : MAROON_B}
            )
            for time in self.end_time, self.end_time + self.dt
        ]


        self.play(Write(frac))
        self.play(Write(rise_over_run))
        self.dither()
        def input_point_line_update(line, alpha):
            time = interpolate(self.start_time, self.end_time, alpha)
            line.put_start_and_end_on(
                self.coords_to_point(time, 0),
                self.input_to_graph_point(time),
            )
        def ds_dt_group_update(group, alpha):
            time = interpolate(self.start_time, self.end_time, alpha)
            new_group = get_ds_dt_group(time)
            Transform(group, new_group).update(1)
        self.play(
            UpdateFromAlphaFunc(input_point_line, input_point_line_update),
            UpdateFromAlphaFunc(ds_dt_group, ds_dt_group_update),
            UpdateFromFunc(self.little_rectangle, align_little_rectangle_on_ds_dt_group),
            run_time = 6,
        )
        self.play(FadeOut(input_point_line))
        self.dither()
        self.play(FadeOut(rise_over_run))
        self.play(Write(of_t))
        self.dither(2)
        self.play(ShowCreation(velocity_graph))
        velocity_label = self.label_graph(
            velocity_graph, 
            label = "v(t)",
            proportion = 0.6,
            direction = DOWN+LEFT,
            buff = SMALL_BUFF
        )
        self.dither(2)
        self.play(Write(dt_choice))
        self.dither()
        for anim_class in FadeIn, FadeOut:
            self.play(anim_class(
                t_tick_marks, submobject_mode = "lagged_start",
                run_time = 2
            ))
        self.play(
            Write(equals),
            Write(numerator)
        )
        self.dither()

        self.play(ShowCreation(v_line_at_t))
        self.dither()
        self.play(ShowCreation(v_line_at_t_plus_dt))
        self.dither()
        self.play(*map(FadeOut, [v_line_at_t, v_line_at_t_plus_dt]))
        self.play(
            Write(frac_line),
            Write(lower_dt)
        )
        self.dither(2)

        #Show different curves
        self.disactivate_zooming()
        self.remove(ds_dt_group)

        self.graph.save_state()
        velocity_graph.save_state()
        velocity_label.save_state()
        def steep_slope(t):
            return 100*smooth(t/10., inflection = 25)
        def sin_wiggle(t):
            return (10/(2*np.pi/10.))*(np.sin(2*np.pi*t/10.) + 2*np.pi*t/10.)
        def double_smooth_graph_function(t):
            if t < 5:
                return 50*smooth(t/5.)
            else:
                return 50*(1+smooth((t-5)/5.))
        graph_funcs = [
            steep_slope,
            sin_wiggle,            
            double_smooth_graph_function,
        ]
        for graph_func in graph_funcs:
            new_graph = self.graph_function(
                graph_func,
                color = DISTANCE_COLOR,
                is_main_graph = False
            )
            self.remove(new_graph)
            new_velocity_graph = self.get_derivative_graph(
                graph = new_graph,
            )

            self.play(Transform(self.graph, new_graph))
            self.play(Transform(velocity_graph, new_velocity_graph))
            self.dither(2)
        self.play(self.graph.restore)
        self.play(
            velocity_graph.restore,
            velocity_label.restore,
        )

        #Pause and reflect
        randy = Randolph()
        randy.to_corner(DOWN+LEFT).shift(2*RIGHT)
        randy.look_at(frac_line)

        self.play(FadeIn(randy))
        self.play(randy.change_mode, "pondering")
        self.dither()
        self.play(Blink(randy))
        self.play(randy.change_mode, "thinking")
        self.dither()
        self.play(Blink(randy))
        self.dither()

class DefineTrueDerivative(Scene):
    def construct(self):
        title = TextMobject("The true derivative")
        title.to_edge(UP)

        lhs = TexMobject("\\frac{ds}{dt}(t) = ")
        VGroup(*lhs[:2]).highlight(DISTANCE_COLOR)
        VGroup(*lhs[3:5]).highlight(TIME_COLOR)
        lhs.shift(3*LEFT+UP)

        dt_rhs = self.get_fraction("dt")
        numerical_rhs_list = [
            self.get_fraction("0.%s1"%("0"*x))
            for x in range(7)
        ]
        for rhs in [dt_rhs] + numerical_rhs_list:
            rhs.next_to(lhs, RIGHT)

        brace, dt_to_zero = self.get_brace_and_text(dt_rhs)

        self.add(lhs, dt_rhs)
        self.play(Write(title))
        self.dither()
        dt_rhs.save_state()
        for num_rhs in numerical_rhs_list:
            self.play(Transform(dt_rhs, num_rhs))
        self.dither()
        self.play(dt_rhs.restore)
        self.play(
            GrowFromCenter(brace),
            Write(dt_to_zero)
        )
        self.dither()

    def get_fraction(self, dt_string):
        tex_mob = TexMobject(
            "\\frac{s(t + %s) - s(t)}{%s}"%(dt_string, dt_string)
        )
        part_lengths = [
            0,
            len("s(t+"),
            1,#1 and -1 below are purely for transformation quirks
            len(dt_string)-1,
            len(")-s(t)_"),#Underscore represents frac_line
            1,
            len(dt_string)-1,
        ]
        pl_cumsum = np.cumsum(part_lengths)
        result = VGroup(*[
            VGroup(*tex_mob[i1:i2])
            for i1, i2 in zip(pl_cumsum, pl_cumsum[1:])
        ])
        VGroup(*result[1:3]+result[4:6]).highlight(TIME_COLOR)
        return result

    def get_brace_and_text(self, deriv_frac):
        brace = Brace(VGroup(deriv_frac), DOWN)
        dt_to_zero = brace.get_text("$dt \\to 0$")
        VGroup(*dt_to_zero[:2]).highlight(TIME_COLOR)
        return brace, dt_to_zero

class SecantLineToTangentLine(GraphCarTrajectory, DefineTrueDerivative):
    CONFIG = {
        "start_time" : 6,
        "end_time" : 2,
        "alt_end_time" : 10,
        "start_dt" : 2,
        "end_dt" : 0.01,
        "secant_line_length" : 10,

    }
    def construct(self):
        self.setup_axes(animate = False)
        self.remove(self.y_axis_label_mob, self.x_axis_label_mob)
        self.add_derivative_definition(self.y_axis_label_mob)
        self.add_graph()
        self.show_tangent_line()
        self.best_constant_approximation_around_a_point()

    def get_ds_dt_group(self, dt, animate = False):
        points = [
            self.input_to_graph_point(time)
            for time in self.curr_time, self.curr_time+dt
        ]
        dots = map(Dot, points)
        for dot in dots:
            dot.scale_in_place(0.5)
        secant_line = Line(*points)
        secant_line.highlight(VELOCITY_COLOR)
        secant_line.scale_in_place(
            self.secant_line_length/secant_line.get_length()
        )

        interim_point = points[1][0]*RIGHT + points[0][1]*UP
        dt_line = Line(points[0], interim_point, color = TIME_COLOR)
        ds_line = Line(interim_point, points[1], color = DISTANCE_COLOR)
        dt = TexMobject("dt")
        dt.highlight(TIME_COLOR)
        if dt.get_width() > dt_line.get_width():
            dt.scale(
                dt_line.get_width()/dt.get_width(),
                about_point = dt.get_top()
            )
        dt.next_to(dt_line, DOWN, buff = SMALL_BUFF)
        ds = TexMobject("ds")
        ds.highlight(DISTANCE_COLOR)
        if ds.get_height() > ds_line.get_height():
            ds.scale(
                ds_line.get_height()/ds.get_height(),
                about_point = ds.get_left()
            )
        ds.next_to(ds_line, RIGHT, buff = SMALL_BUFF)

        group = VGroup(
            secant_line, 
            ds_line, dt_line,
            ds, dt,
            *dots
        )
        if animate:
            self.play(
                ShowCreation(dt_line),
                Write(dt),
                ShowCreation(dots[0]),                
            )
            self.play(
                ShowCreation(ds_line),
                Write(ds),
                ShowCreation(dots[1]),                
            )
            self.play(
                ShowCreation(secant_line),
                Animation(VGroup(*dots))
            )
        return group

    def add_graph(self):
        def double_smooth_graph_function(t):
            if t < 5:
                return 50*smooth(t/5.)
            else:
                return 50*(1+smooth((t-5)/5.))
        graph = self.graph_function(
            double_smooth_graph_function,
            animate = False
        )
        self.label_graph(
            graph, "s(t)", 
            proportion = 1, 
            direction = DOWN+RIGHT, 
            buff = SMALL_BUFF,
            animate = False
        )

    def add_derivative_definition(self, target_upper_left):
        deriv_frac = self.get_fraction("dt")
        lhs = TexMobject("\\frac{ds}{dt}(t)=")
        VGroup(*lhs[:2]).highlight(DISTANCE_COLOR)
        VGroup(*lhs[3:5]).highlight(TIME_COLOR)
        lhs.next_to(deriv_frac, LEFT)
        brace, text = self.get_brace_and_text(deriv_frac)
        deriv_def = VGroup(lhs, deriv_frac, brace, text)
        deriv_word = TextMobject("Derivative")        
        deriv_word.next_to(deriv_def, UP, buff = 2*MED_BUFF)
        deriv_def.add(deriv_word)
        rect = Rectangle(color = WHITE)
        rect.replace(deriv_def, stretch = True)
        rect.scale_in_place(1.2)
        deriv_def.add(rect)
        deriv_def.scale(0.7)
        deriv_def.move_to(target_upper_left, UP+LEFT)
        self.add(deriv_def)
        return deriv_def

    def show_tangent_line(self):
        self.curr_time = self.start_time

        ds_dt_group = self.get_ds_dt_group(2, animate = True)
        self.dither()
        def update_ds_dt_group(ds_dt_group, alpha):
            new_dt = interpolate(self.start_dt, self.end_dt, alpha)
            new_group = self.get_ds_dt_group(new_dt)
            Transform(ds_dt_group, new_group).update(1)
        self.play(
            UpdateFromAlphaFunc(ds_dt_group, update_ds_dt_group),
            run_time = 8
        )
        self.dither()
        def update_as_tangent_line(ds_dt_group, alpha):
            self.curr_time = interpolate(self.start_time, self.end_time, alpha)
            new_group = self.get_ds_dt_group(self.end_dt)
            Transform(ds_dt_group, new_group).update(1)
        self.play(
            UpdateFromAlphaFunc(ds_dt_group, update_as_tangent_line),
            run_time = 8,
            rate_func = there_and_back
        )
        self.dither()
        what_dt_is_not_text = self.what_this_is_not_saying()
        self.dither()
        self.play(
            UpdateFromAlphaFunc(ds_dt_group, update_ds_dt_group),
            run_time = 8,
            rate_func = lambda t : 1-there_and_back(t)
        )
        self.dither()
        self.play(FadeOut(what_dt_is_not_text))

        v_line = self.get_vertical_line_to_graph(
            self.curr_time,
            line_class = Line,
            line_kwargs = {
                "color" : MAROON_B,
                "stroke_width" : 3
            }
        )
        def v_line_update(v_line):
            v_line.put_start_and_end_on(
                self.coords_to_point(self.curr_time, 0),
                self.input_to_graph_point(self.curr_time),
            )
            return v_line
        self.play(ShowCreation(v_line))
        self.dither()

        original_end_time = self.end_time
        for end_time in self.alt_end_time, original_end_time, self.start_time:
            self.end_time = end_time
            self.play(
                UpdateFromAlphaFunc(ds_dt_group, update_as_tangent_line),
                UpdateFromFunc(v_line, v_line_update),
                run_time = abs(self.curr_time-self.end_time),
            )
            self.start_time = end_time
        self.play(FadeOut(v_line))

    def what_this_is_not_saying(self):
        phrases = [
            TextMobject(
                "$dt$", "is", "not", s
            )
            for s in "``infinitely small''", "0"
        ]
        for phrase in phrases:
            phrase[0].highlight(TIME_COLOR)
            phrase[2].highlight(RED)
        phrases[0].shift(DOWN+2*RIGHT)
        phrases[1].next_to(phrases[0], DOWN, aligned_edge = LEFT)

        for phrase in phrases:
            self.play(Write(phrase))
        return VGroup(*phrases)

    def best_constant_approximation_around_a_point(self):
        words = TextMobject("""
            Best constant 
            approximation
            around a point
        """)
        words.next_to(self.x_axis, UP, aligned_edge = RIGHT)
        circle = Circle(
            radius = 0.25,
            color = WHITE
        ).shift(self.input_to_graph_point(self.curr_time))

        self.play(Write(words))
        self.play(ShowCreation(circle))        
        self.dither()

class LeadIntoASpecificExample(TeacherStudentsScene, SecantLineToTangentLine):
    def setup(self):
        TeacherStudentsScene.setup(self)

    def construct(self):
        dot = Dot() #Just to coordinate derivative definition
        dot.to_corner(UP+LEFT, buff = SMALL_BUFF)
        deriv_def = self.add_derivative_definition(dot)
        self.remove(deriv_def)

        self.teacher_says("An example \\\\ should help.")
        self.dither()
        self.play(
            Write(deriv_def),
            *it.chain(*[
                [pi.change_mode, "thinking", pi.look_at, dot]
                for pi in self.get_students()
            ])
        )
        self.random_blink(3)
        # self.teacher_says(
        #     """
        #     The idea of 
        #     ``approaching''
        #     actually makes 
        #     things easier
        #     """,
        #     height = 3,
        #     target_mode = "hooray"
        # )
        # self.dither(2)

class TCubedExample(SecantLineToTangentLine):
    CONFIG = {
        "y_axis_label" : "Distance",
        "y_min" : 0,
        "y_max" : 16,
        "y_tick_frequency" : 1,
        "y_labeled_nums" : range(0, 17, 2),
        "x_min" : 0,
        "x_max" : 4,
        "x_labeled_nums" : range(1, 5),
        "graph_origin" : 2.5*DOWN + 6*LEFT,
        "start_time" : 2,
        "start_dt" : 0.25,
        "secant_line_length" : 0,
    }
    def construct(self):
        self.draw_graph()
        self.show_vertical_lines()
        self.bear_with_me()
        self.add_ds_dt_group()
        self.brace_for_details()
        self.show_expansion()

    def draw_graph(self):
        self.setup_axes(animate = False)
        self.x_axis_label_mob.shift(0.5*DOWN)
        # self.y_axis_label_mob.next_to(self.y_axis, UP)
        graph = self.graph_function(lambda t : t**3, animate = True)
        self.label_graph(
            graph,
            label = "s(t) = t^3",
            proportion = 0.62,
            direction = LEFT,
            buff = SMALL_BUFF
        )
        self.dither()

    def show_vertical_lines(self):
        for t in 1, 2:
            v_line = self.get_vertical_line_to_graph(
                t, line_kwargs = {"color" : WHITE}
            )
            brace = Brace(v_line, RIGHT)
            text = TexMobject("%d^3 = %d"%(t, t**3))
            text.next_to(brace, RIGHT)
            text.shift(0.2*UP)
            group = VGroup(v_line, brace, text)
            if t == 1:
                self.play(ShowCreation(v_line))
                self.play(
                    GrowFromCenter(brace),
                    Write(text)
                )
                last_group = group
            else:
                self.play(Transform(last_group, group))
            self.dither()
        self.play(FadeOut(last_group))

    def bear_with_me(self):
        morty = Mortimer()
        morty.to_corner(DOWN+RIGHT)

        self.play(FadeIn(morty))
        self.play(PiCreatureSays(
            morty, "Bear with \\\\ me here",
            target_mode = "sassy"
        ))
        self.play(Blink(morty))
        self.dither()
        self.play(*map(
            FadeOut, 
            [morty, morty.bubble, morty.bubble.content]
        ))

    def add_ds_dt_group(self):
        self.curr_time = self.start_time
        self.curr_dt = self.start_dt
        ds_dt_group = self.get_ds_dt_group(dt = self.start_dt)
        v_lines = self.get_vertical_lines()

        lhs = TexMobject("\\frac{ds}{dt}(2) = ")
        lhs.next_to(ds_dt_group, UP+RIGHT, buff = 2*MED_BUFF)
        ds = VGroup(*lhs[:2])
        dt = VGroup(*lhs[3:5])
        ds.highlight(DISTANCE_COLOR)
        dt.highlight(TIME_COLOR)
        ds.target, dt.target = ds_dt_group[3:5]
        for mob in ds, dt:
            mob.save_state()
            mob.move_to(mob.target)

        rhs = TexMobject(
            "\\frac{s(2+dt) - s(2)}{dt}"
        )
        rhs.next_to(lhs[-1])
        VGroup(*rhs[4:6]).highlight(TIME_COLOR)
        VGroup(*rhs[-2:]).highlight(TIME_COLOR)
        numerator = VGroup(*rhs[:-3])
        non_numerator = VGroup(*rhs[-3:])
        numerator_non_minus = VGroup(*numerator)
        numerator_non_minus.remove(rhs[7])
        s_pair = rhs[0], rhs[8]
        lp_pair = rhs[6], rhs[11]
        for s, lp in zip(s_pair, lp_pair):
            s.target = TexMobject("3").scale(0.7)
            s.target.move_to(lp.get_corner(UP+RIGHT), LEFT)



        self.play(Write(ds_dt_group, run_time = 2))
        self.play(
            FadeIn(lhs),
            *[mob.restore for mob in ds, dt]
        )
        self.play(ShowCreation(v_lines[0]))
        self.dither()
        self.play(
            dt.target.scale_in_place, 1.2,
            rate_func = there_and_back
        )
        self.dither(2)
        self.play(Write(numerator))
        self.play(ShowCreation(v_lines[1]))
        self.dither()
        self.play(Write(non_numerator))
        self.dither(2)
        self.play(
            *map(MoveToTarget, s_pair),
            **{
                "path_arc" : -np.pi/2
            }
        )
        self.play(numerator_non_minus.shift, 0.2*LEFT)
        self.dither()

        self.vertical_lines = v_lines
        self.ds_dt_group = ds_dt_group
        self.lhs = lhs
        self.rhs = rhs

    def get_vertical_lines(self):
        return VGroup(*[
            self.get_vertical_line_to_graph(
                time,
                line_class = DashedLine,
                line_kwargs = {
                    "color" : WHITE,
                    "dashed_segment_length" : 0.05,
                }
            )
            for time in self.start_time, self.start_time+self.start_dt
        ])

    def brace_for_details(self):
        brace_yourself = TextMobject(
            "(Brace yourself for details)"
        )
        brace_yourself.next_to(
            self.lhs, DOWN, 
            buff = LARGE_BUFF,
            aligned_edge = LEFT
        )
        self.play(FadeIn(brace_yourself))
        self.dither()
        self.play(FadeOut(brace_yourself))

    def show_expansion(self):
        expression = TexMobject("""
            \\frac{
                2^3 + 
                3 (2)^2 dt + 
                3 (2)(dt)^2 + 
                (dt)^3
                - 2^3
            }{dt}
        """)
        expression.scale_to_fit_width(
            VGroup(self.lhs, self.rhs).get_width()
        )
        expression.next_to(
            self.lhs, DOWN, 
            aligned_edge = LEFT,
            buff = LARGE_BUFF
        )
        term_lens = [
            len("23+"),
            len("3(2)2dt+"),
            len("3(2)(dt)2+"),
            len("(dt)3"),
            len("-23"),
            len("_"),#frac bar
            len("dt"),
        ]
        terms = [
            VGroup(*expression[i1:i2])
            for i1, i2 in zip(
                [0]+list(np.cumsum(term_lens)),
                np.cumsum(term_lens)
            )
        ]

        dts = [
            VGroup(*terms[1][-3:-1]),
            VGroup(*terms[2][5:7]),
            VGroup(*terms[3][1:3]),
            terms[-1]
        ]
        VGroup(*dts).highlight(TIME_COLOR)

        two_cubed_terms = terms[0], terms[4]

        for term in terms:
            self.play(FadeIn(term))
            self.dither()

        #Cancel out two_cubed terms
        self.play(*it.chain(*[
            [
                tc.scale, 1.3, tc.get_corner(vect),
                tc.highlight, RED
            ]
            for tc, vect in zip(
                two_cubed_terms, 
                [DOWN+RIGHT, DOWN+LEFT]
            )
        ]))
        self.play(*map(FadeOut, two_cubed_terms))
        numerator = VGroup(*terms[1:4])
        self.play(
            numerator.scale, 1.3, numerator.get_bottom(),
            terms[-1].scale, 1.3, terms[-1].get_top()
        )

        #Cancel out dt
        #TODO





































