module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    fontFamily: {
      sans: ['Helvetica Neue LT Pro', 'Arial', 'sans-serif'],
    },
    colors: {
      transparent: 'transparent',
      white: '#FFFFFF',
      black: '#001215',
      coolgray: {
        20: '#E9E9EF',
        60: '#5c7781',
        100: '#001215',
        DEFAULT: '#5c7781',
      },
      zueriblue: {
        light: '#6496FF',
        DEFAULT: '#0F05A0',
        dark: '#090036',
      },
      orange: {
        DEFAULT: '#DF4808',
      },
      green: {
        DEFAULT: '#2D9225',
      },
      red: {
        DEFAULT: '#B30058',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
