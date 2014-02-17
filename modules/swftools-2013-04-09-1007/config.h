#ifndef __config_h__
#define __config_h__

/* Define to empty if the keyword does not work.  */
// const is not set

/* Define as __inline if that's what the C compiler calls it.  */
// inline is not set

/* Define to `long' if <sys/types.h> doesn't define.  */
// off_t is not set

/* Define to `unsigned' if <sys/types.h> doesn't define.  */
// size_t is not set

#define SIZEOF_SIGNED_CHAR 1
#define SIZEOF_SIGNED_SHORT 2
#define SIZEOF_SIGNED 4
#define SIZEOF_SIGNED_LONG_LONG 8
#define SIZEOF_VOIDP 4

/* Define if you have the ANSI C header files.  */
#define STDC_HEADERS 1

/* Define if your <sys/time.h> declares struct tm.  */
// TM_IN_SYS_TIME is not set

/* Define if you have the time() function */
#define HAVE_TIME 1

/* Define if you have the time.h header file */
// HAVE_TIME_H is not set

/* Define if you have the sys/time.h header file */
// HAVE_SYS_TIME_H is not set

/* Define if you have the sys/resource.h header file */
// HAVE_SYS_RESOURCE_H is not set

/* Define if you have the malloc.h header file */
// HAVE_MALLOC_H is not set

/* Define if you have the getrusage function */
#define HAVE_GETRUSAGE 1

/* Define if you have the mallinfo function */
#define HAVE_MALLINFO 1


/* Define if you have the unistd.h header file */
// HAVE_UNISTD_H is not set

/* Define if you have the open64 function.  */
#define HAVE_OPEN64 1

/* Define if you have the lrand48 function.  */
#define HAVE_LRAND48 1

/* Define if you have the popen function.  */
#define HAVE_POPEN 1

/* Define if you have the bcopy function.  */
#define HAVE_BCOPY 1

/* Define if you have the bzero function.  */
#define HAVE_BZERO 1

/* Define if you have the rand function.  */
#define HAVE_RAND 1

/* Define if you have the srand function.  */
#define HAVE_SRAND 1

/* Define if you have the srand48 function.  */
#define HAVE_SRAND48 1

/* Define if you have the calloc function.  */
#define HAVE_CALLOC 1

/* Define if you have the stat function.  */
#define HAVE_STAT 1

/* Define if you have the mmap function.  */
#define HAVE_MMAP 1

/* Define if you have the <dirent.h> header file.  */
// HAVE_DIRENT_H is not set

/* Define if you have the <assert.h> header file.  */
// HAVE_ASSERT_H is not set

/* Define if you have the <signal.h> header file.  */
// HAVE_SIGNAL_H is not set

/* Define if you have the <pthread.h> header file.  */
// HAVE_PTHREAD_H is not set

/* Define if you have the <jpeglib.h> header file.  */
// HAVE_JPEGLIB_H is not set

/* Define if you have the <ndir.h> header file.  */
// HAVE_NDIR_H is not set

/* Define if you have the <sys/dir.h> header file.  */
// HAVE_SYS_DIR_H is not set

/* Define if you have the <sys/ndir.h> header file.  */
// HAVE_SYS_NDIR_H is not set

/* Define if you have the <sys/io.h> header file.  */
// HAVE_IO_H is not set

/* Define if you have the <sys/bsdtypes.h> header file.  */
// HAVE_SYS_BSDTYPES_H is not set

/* Define if you have the <sys/stat.h> header file.  */
// HAVE_SYS_STAT_H is not set

/* Define if you have the <sys/mman.h> header file.  */
// HAVE_SYS_MMAN_H is not set

/* Define if you have the <sys/types.h> header file.  */
// HAVE_SYS_TYPES_H is not set

/* Define if you have the <t1lib.h> header file.  */
/* #undef HAVE_T1LIB_H */

/* Define if you have the <zlib.h> header file.  */
// HAVE_ZLIB_H is not set

/* Define if you have the <zzip/lib.h> header file.  */
// HAVE_ZZIP_LIB_H is not set

/* Define if you have the <pdflib.h> header file.  */
// HAVE_PDFLIB_H is not set

/* Define if you have the <avifile/version.h> header file.  */
// HAVE_AVIFILE_VERSION_H is not set

/* Define if you have the <freetype/ft2build.h> header file.  */
// HAVE_FT2BUILD_H is not set

/* Define if you have the <version.h> header file.  */
// HAVE_VERSION_H is not set

/* Define if you have the OpenGL header files */
// HAVE_GL_GL_H is not set
// HAVE_GL_GLUT_H is not set

/* Define if you have the OpenGL libraries */
// HAVE_LIBGL is not set
// HAVE_LIBGLU is not set
// HAVE_LIBGLUT is not set

/* Define if OpenGL seems to work */
#define HAVE_OPENGL 1

/* Define if you use poppler */
// HAVE_POPPLER is not set

/* Define to 1 if you have the `poppler' library (-lpoppler). */
// HAVE_LIBPOPPLER is not set

/* Define to 1 if you have the <OutputDev.h> header file. */
// HAVE_OUTPUTDEV_H is not set

/* Define if you have the jpeg library (-ljpeg).  */
// HAVE_LIBJPEG is not set

/* Define if you have the pdf library (-lpdf).  */
// HAVE_LIBPDF is not set

/* Define if you have the zzip library (-lzzip). */
// HAVE_LIBZZIP is not set

/* Define if you have the m library (-lm).  */
// HAVE_LIBM is not set

/* Define if you have the t1 library (-lt1).  */
/* #undef HAVE_LIBT1 */

/* Define if you have the z library (-lz).  */
// HAVE_LIBZ is not set

/* Name of package */
#define PACKAGE "swftools"

/* Version number of package */
#define VERSION "2013-04-09-1007"

/* Typedefs */
#define boolean int

/* use gzip/uncompress */
// USE_GZIP is not set

/* let ttf2pt1 use libfreetype */
// USE_FREETYPE is not set

/* have/use freetype library */
// HAVE_FREETYPE is not set
// HAVE_FREETYPE_FREETYPE_H is not set

/* have/use freetype library */
#define HAVE_AVIFILE 1

// HAVE_FONTCONFIG_H is not set
// HAVE_FONTCONFIG is not set

// HAVE_FFTW3_H is not set

// HAVE_FFTW3 is not set

/* have/use internal l.a.m.e. mp3 library */
// HAVE_LAME is not set

/* whether python-imaging was found */
#define HAVE_PYTHON_IMAGING 1

/* system() can handle command substitution */
// SYSTEM_BACKTICKS is not set

/* Define to 1 if this machine has network byte order*/
// WORDS_BIGENDIAN is not set

// LOWERCASE_UPPERCASE is not set

/* Define to 0 on non-windows systems */
// O_BINARY is not set

#ifdef HAVE_ZLIB_H
#ifdef HAVE_LIBZ
#define HAVE_ZLIB
#endif
#endif

#ifdef HAVE_JPEGLIB_H
#ifdef HAVE_LIBJPEG
#define HAVE_JPEGLIB
#endif
#endif

#ifdef HAVE_FT2BUILD_H
#define HAVE_FREETYPE_H 1
#endif

/* #ifdef HAVE_T1LIB_H */
/* #ifdef HAVE_LIBT1 */
/* #define HAVE_T1LIB */
/* #endif */
/* #endif */

#ifdef HAVE_GL_GL_H
#ifdef HAVE_GL_GLUT_H
#ifdef HAVE_OPENGL
#define USE_OPENGL
#endif
#endif
#endif

#ifdef HAVE_POPPLER
#define GString GooString
#define GHash GooHash
#endif

#ifdef HAVE_ZZIP_LIB_H
#ifdef HAVE_LIBZZIP
#define HAVE_ZZIP 1
#endif
#endif

//#ifdef HAVE_BUILTIN_EXPECT
#if defined(__GNUC__) && (__GNUC__ > 2) && defined(__OPTIMIZE__)
# define likely(x)      __builtin_expect((x), 1)
# define unlikely(x)    __builtin_expect((x), 0)
#else
# define likely(x)      (x)
# define unlikely(x)    (x)
#endif

#endif
// python:lib 
