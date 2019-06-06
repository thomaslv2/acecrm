$('.item .title').click(function () {
    // $(this).next().toggleClass('hide')

    $(this).next().removeClass('hide').parent().siblings().find('.body').addClass('hide')
})