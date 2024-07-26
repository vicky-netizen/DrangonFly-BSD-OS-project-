

$(document).ready(function() {
  const progressBar = $('progress');
  const progressLabel = $('.progress-label');
  const iframe = $('#instagram-frame')[0];

  const setPercent = () => {
    const win = iframe.contentWindow;
    const doc = iframe.contentDocument;
    return Math.round(win.pageYOffset / (doc.body.scrollHeight - win.innerHeight) * 100);
  };

  const updateProgress = () => {
    progressLabel.text(setPercent() + '%');
    progressBar.attr({ value: iframe.contentWindow.pageYOffset });
  };

  $(iframe).on('load', function() {
    updateProgress();
    $(this.contentWindow).on('scroll', updateProgress);
  });
});



$(document).ready(function() {
  const win = $(window);
  const doc = $(document);
  const progressBar = $('progress');
  const progressLabel = $('.progress-label');
  const setValue = () => win.scrollTop();
  const setMax = () => doc.height() - win.height();
  const setPercent = () => Math.round(win.scrollTop() / (doc.height() - win.height()) * 100);
  
  progressLabel.text(setPercent() + '%');
  progressBar.attr({ value: setValue(), max: setMax() });

  doc.on('scroll', () => {
    progressLabel.text(setPercent() + '%');
    progressBar.attr({ value: setValue() });
  });
  
  win.on('resize', () => {
    progressLabel.text(setPercent() + '%');
    progressBar.attr({ value: setValue(), max: setMax() });
  })
});