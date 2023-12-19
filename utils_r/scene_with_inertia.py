class SceneWithInertia:
    def __init__(self, dy_law, inertia):
        self.full_signal =
        self.pos_start =
        self.pos_end =
        self.neg_start =
        self.neg_end =

        self.dy_law = dy_law
        self.inertia = inertia

    def get_r(self):
        pass

    def get_p_of_so_good_in_region_segmentwise(self, segment_len):
        pass

    def measure_p_of_so_good_in_segment(self, start_index, len_segment):
        pass

    def check_prediction_err_for_segment(self, start_index, len_segment):
        pass

    def create_prediction_for_next_points(self, v_real_start, num_next_points):
        pass

    def get_err_distr_for_segment(self, v_list_real):
        pass