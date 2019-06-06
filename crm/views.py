#
#
#
#
#
#
# userlist = [{'name': 'alex-{}'.format(i), 'pwd': 'dba-{}'.format(i)} for i in range(1, 302)]
#
#
# # def user_list(request):
# #     page_num = request.GET.get('page')
# #     try:
# #         page_num = int(page_num)
# #         if page_num <= 1:
# #             page_num = 1
# #     except Exception as e:
# #         page_num = 1
# #     all_count = len(userlist)
# #     per_num = 10
# #     total_page_num, more = divmod(all_count, per_num)
# #     if more:
# #         total_page_num += 1
# #     max_show = 11
# #     half_show = max_show // 2
# #
# #     if total_page_num < max_show:
# #         page_start = 1
# #         page_end = total_page_num + 1
# #     elif page_num <= half_show:
# #         page_start = 1
# #         page_end = max_show + 1
# #     elif page_num > total_page_num - half_show:
# #         page_start = total_page_num - max_show + 1
# #         page_end = total_page_num + 1
# #     else:
# #         page_start = page_num - half_show
# #         page_end = page_num + half_show + 1
# #
# #     start = per_num * (page_num - 1)
# #     end = per_num * page_num
# #
# #     page_list = []
# #     if page_num == 1:
# #         page_list.append('<li class="disabled"><a>上一页</a></li>'.format(page_num - 1))
# #     else:
# #         page_list.append('<li><a href="?page={}">上一页</a></li>'.format(page_num - 1))
# #
# #     for i in range(page_start, page_end):
# #         if i == page_num:
# #             page_list.append('<li class ="active"><a href="?page={}">{}</a></li>'.format(i, i))
# #         else:
# #             page_list.append('<li><a href="?page={}">{}</a></li>'.format(i, i))
# #     if page_num == total_page_num:
# #         page_list.append('<li class="disabled"><a ">下一页</a></li>'.format(page_num + 1))
# #     else:
# #         page_list.append('<li><a href="?page={}">下一页</a></li>'.format(page_num + 1))
# #
# #     page_html = ' '.join(page_list)
# #
# #     return render(request, 'user_list.html', {'user_list': userlist[start:end], 'page_html': page_html})
#
# from crm.utils.pagination import Pagination
# def user_list(request):
#     page_num=request.GET.get('page')
#     page=Pagination(page_num,len(userlist))
#     return render(request, 'user_list.html', {'user_list': userlist[page.start:page.end], 'page_html': page.page_html})
