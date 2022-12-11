FROM denoland/deno:alpine

RUN deno install -f --name silverbullet -A --unstable https://get.silverbullet.md

# RUN mkdir /space
# WORKDIR /space
# RUN chown deno:deno /space

# /deno-dir/deps needs write permissions for deno user or sb will not run
RUN chown deno:deno /deno-dir/deps

# deno user id is 1000 in alpine image
USER deno

EXPOSE 3000

CMD ["silverbullet", "/space"]
