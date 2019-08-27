'use strict';
var gulp         = require('gulp');
var sass         = require('gulp-sass');
var livereload   = require('gulp-livereload');
var autoprefixer = require('autoprefixer');
var postcss      = require('gulp-postcss');
var csscomb      = require('gulp-csscomb');

gulp.task('sass', function(){
    gulp.src('scss/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(sass({outputStyle: 'expanded'}))
        .pipe(postcss([ autoprefixer() ]))
        .pipe(csscomb())
        .pipe(gulp.dest('css'));
});

gulp.task('watch-sass', function(){
    livereload.listen();
    gulp.watch('scss/**/*.scss', ['sass']);
});

gulp.task('default', ['sass', 'watch-sass']);