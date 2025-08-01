FROM ruby:3.1-slim

# Install system dependencies needed for native gem compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    pkg-config \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/jekyll
COPY Gemfile /srv/jekyll/Gemfile

# Install gems
RUN bundle install

CMD ["bundle", "exec", "jekyll", "serve", "--watch", "--host", "0.0.0.0"]
