var gulp = require('gulp'),
    p = require('gulp-load-plugins')();

gulp.task('styles', function () {
    gulp.src('./youmu/static/sass/base.scss')
    .pipe(p.sass({
        // outputStyle: 'compressed'    // Uncomment to use compressed style in production
    }))
    .pipe(p.autoprefixer({
        browsers: ['last 3 versions'],
        cascade: false
    }))
    .pipe(gulp.dest('./youmu/static/css/'))
    .pipe(p.livereload());
});

gulp.task('html', function() {
    gulp.src('youmu/templates/**/*.html')
    .pipe(p.htmlhint())
    .pipe(p.htmlhint.reporter())
    .pipe(p.livereload());
});

gulp.task('js', function() {
    gulp.src('youmu/static/js/*.js')
    .pipe(p.jshint())
    .pipe(p.jshint.reporter('default'))
    .pipe(p.livereload());
});

gulp.task('watch', function() {
    p.livereload.listen();

    gulp.watch('./youmu/static/sass/**/*.scss', ['styles']);
    gulp.watch('./youmu/templates/**/*.html', ['html']);
    gulp.watch('./youmu/static/js/*.js', ['js']);
});

gulp.task('default', function() {
    gulp.start('watch');
});
