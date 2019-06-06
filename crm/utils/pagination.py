from django.utils.safestring import mark_safe


class Pagination:
    def __init__(self, page_num, all_count, params, per_num=10, max_show=11):
        try:
            self.page_num = int(page_num)
            if self.page_num <= 1:
                self.page_num = 1
        except Exception as e:
            self.page_num = 1

        self.params=params
        self.all_count = all_count
        self.per_num = per_num
        self.total_page_num, more = divmod(all_count, per_num)
        if more:
            self.total_page_num += 1
        self.max_show = max_show
        self.half_show = self.max_show // 2

    @property
    def start(self):
        return self.per_num * (self.page_num - 1)

    @property
    def end(self):
        return self.per_num * self.page_num

    @property
    def page_html(self):
        if self.total_page_num < self.max_show:
            page_start = 1
            page_end = self.total_page_num + 1
        elif self.page_num <= self.half_show:
            page_start = 1
            page_end = self.max_show + 1
        elif self.page_num > self.total_page_num - self.half_show:
            page_start = self.total_page_num - self.max_show + 1
            page_end = self.total_page_num + 1
        else:
            page_start = self.page_num - self.half_show
            page_end = self.page_num + self.half_show + 1

        page_list = []
        if self.page_num == 1:
            page_list.append('<li class="disabled"><a>上一页</a></li>')
        else:
            self.params['page'] = self.page_num - 1
            page_list.append('<li><a href="?{}">上一页</a></li>'.format(self.params.urlencode()))

        for i in range(page_start, page_end):
            self.params['page'] = i
            if i == self.page_num:
                page_list.append('<li class ="active"><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))
            else:
                page_list.append('<li><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))
        if self.page_num == self.total_page_num:
            page_list.append('<li class="disabled"><a ">下一页</a></li>')
        else:
            self.params['page'] = self.page_num + 1
            page_list.append('<li><a href="?{}">下一页</a></li>'.format(self.params.urlencode()))

        return mark_safe(' '.join(page_list))
