function insertImagesIntoArticleBody(originalContent: any, articleBody: any) {
  const imgRegex =
    /<img\s+[^>]*src=["']([^"']+)["'][^>]*alt=["']([^"']+)["'][^>]*>/g;
  let matches;
  let imgData = [];

  // Extract images from original content
  while ((matches = imgRegex.exec(originalContent)) !== null) {
    imgData.push({
      src: matches[1],
      alt: matches[2],
      position: matches.index,
    });
  }

  let updatedArticleBody: any = [];
  let currentIndex = 0;

  // Iterate through articleBody and insert images at correct positions
  articleBody.forEach((entry: any, i: any) => {
    while (
      imgData.length > 0 &&
      imgData[0].position <=
        originalContent.indexOf(entry.content, currentIndex)
    ) {
      let img: any = imgData.shift();
      updatedArticleBody.push({
        id: `img_${i}`,
        type: "image",
        src: img.src,
        alt: img.alt,
      });
    }
    updatedArticleBody.push(entry);
    currentIndex =
      originalContent.indexOf(entry.content, currentIndex) +
      entry.content.length;
  });

  // Append any remaining images
  imgData.forEach((img, i) => {
    updatedArticleBody.push({
      id: `img_extra_${i}`,
      type: "image",
      src: img.src,
      alt: img.alt,
    });
  });

  return updatedArticleBody;
}
