$('.valence-img').on({
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
    $('.valence-img').css({
      'opacity': '0.55'
    });
    $(this).css({
      'opacity': '1'
    });
    $(this).off('mouseleave');
    $('.valence-val').val($(this).attr("name"));
  },
});

$('.control-img').on({
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
    $('.control-img').css({
      'opacity': '0.55'
    });
    $(this).css({
      'opacity': '1'
    });
    $(this).off('mouseleave');
    $('.control-val').val($(this).attr("name"));
  },
});

$('.arousal-img').on({
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
    $('.arousal-img').css({
      'opacity': '0.55'
    });
    $(this).css({
      'opacity': '1'
    });
    $(this).off('mouseleave');
    $('.arousal-val').val($(this).attr("name"));
  },
});