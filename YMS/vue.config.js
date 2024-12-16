module.exports = {
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all',
        maxSize: 200000, // 각 청크의 최대 크기 제한
      },
    },
    performance: {
      hints: false, // 성능 힌트 비활성화 (경고 숨김)
    },
  },
  lintOnSave: false,
  css: {
    loaderOptions: {
      sass: {
        sassOptions: {
          quietDeps: true, // 경고를 무시하도록 설정
        },
      },
    },
  },
};
