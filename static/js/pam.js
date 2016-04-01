$('.pam-img').on({
  mouseover: function() {
    $(this).css({
      'opacity': '1'
    });
    $(this).on('mouseleave', function() {
      $(this).css({
        'opacity': '0.55'
      });
    });
  },
  mouseleave: function() {
    $(this).css({
      'opacity': '0.55'
    });
  },
  click: function() {
    $('.pam-img').css({
      'opacity': '0.55'
    });
    $(this).css({
      'opacity': '1'
    });
    $(this).off('mouseleave');
    $('.pam-val').val($(this).attr("name"));
  },
});

$('.desk-img').on({
  mouseover: function() {
    $(this).css({
      'opacity': '1'
    });
    $(this).on('mouseleave', function() {
      $(this).css({
        'opacity': '0.3'
      });
    });
  },
  mouseleave: function() {
    $(this).css({
      'opacity': '0.3'
    });
  },
  click: function() {
    $('.desk-img').css({
      'opacity': '0.3'
    });
    $(this).css({
      'opacity': '1'
    });
    $(this).off('mouseleave');
    $('.desk-val').val($(this).attr("name"));
  },
});