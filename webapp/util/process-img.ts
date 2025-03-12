function insertImagesIntoArticleBody(
  originalContent: any,
  articleBody: any,
  imgUrls: string[],
  forgery_results: any
) {
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

  console.log(imgData);

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

      // Check if the image URL is not in the provided list of image URLs
      if (!imgUrls.includes(img.src)) {
        updatedArticleBody.unshift({
          id: `img_first_${i}`,
          type: "image",
          src: img.src,
          alt: img.alt,
        });
      } else {
        updatedArticleBody.push({
          id: `img_${i}`,
          type: "image",
          src: img.src,
          alt: img.alt,
        });
      }
    }
    updatedArticleBody.push(entry);
    currentIndex =
      originalContent.indexOf(entry.content, currentIndex) +
      entry.content.length;
  });

  // Append any remaining images
  imgData.forEach((img, i) => {
    // Check if the image URL is not in the provided list of image URLs
    if (!imgUrls.includes(img.src)) {
      updatedArticleBody.unshift({
        id: `img_first_extra_${i}`,
        type: "image",
        src: img.src,
        alt: img.alt,
      });
    } else {
      updatedArticleBody.push({
        id: `img_extra_${i}`,
        type: "image",
        src: img.src,
        alt: img.alt,
      });
    }
  });

  // check imgUrls, append any images that are not in the list
  imgUrls.forEach((imgUrl, i) => {
    if (
      !updatedArticleBody.some(
        (entry: any) => entry.type === "image" && entry.src === imgUrl
      )
    ) {
      updatedArticleBody.unshift({
        id: `img_extra_${i}`,
        type: "image",
        src: imgUrl,
        alt: "",
      });
    }
  });

  let firstSkipped = false;

  // Merge consecutive objects where `to_fact_check` is false
  for (let i = 0; i < updatedArticleBody.length - 1; i++) {
    const currentEntry = updatedArticleBody[i];
    const nextEntry = updatedArticleBody[i + 1];

    //skip the first non image entry and to_fact_check is false
    if (
      currentEntry.type !== "image" &&
      currentEntry.to_fact_check === false &&
      !firstSkipped
    ) {
      firstSkipped = true;
      continue;
    }

    // Check if both entries have `to_fact_check: false` and are consecutive
    if (
      currentEntry.to_fact_check === false &&
      nextEntry.to_fact_check === false &&
      currentEntry.type === nextEntry.type
    ) {
      // Merge their contents (you can decide how to merge them, for now we just combine alt text and add the second entry's id)
      updatedArticleBody[i] = {
        ...currentEntry,
        content: `${currentEntry.content} ${nextEntry.content}`, // example of merging alt text
      };

      // Remove the next entry
      updatedArticleBody.splice(i + 1, 1);

      // Decrement the index to recheck the merged item
      i--;
    }
  }

  // add image forgery result to images
  // const forgery_results_parsed = JSON.parse(forgery_results.raw);
  // updatedArticleBody.forEach((entry: any, i: any) => {
  //   if (entry.type === "image") {
  //     const matchingResult = forgery_results_parsed.find(
  //       (result: any) => result.image_url === entry.image_url
  //     );

  //     entry.forgery_result = matchingResult
  //       ? {
  //           is_forged: matchingResult.is_forged,
  //           is_forged_confidence: matchingResult.is_forged_confidence,
  //         }
  //       : {
  //           is_forged: false,
  //           is_forged_confidence: 0,
  //         };
  //   }
  // });

  return updatedArticleBody;
}

export { insertImagesIntoArticleBody };
