# Puma can serve each request in a thread from an internal thread pool.
# The `threads` method setting takes two numbers: a minimum and maximum.
# Any libraries that use thread pools should be configured to match the maximum value specified for Puma.
# Default is 3 threads for minimum and maximum, this matches the default thread size of Active Record.
max_threads_count = ENV.fetch("RAILS_MAX_THREADS", 5)
min_threads_count = ENV.fetch("RAILS_MIN_THREADS", max_threads_count)
threads min_threads_count, max_threads_count

# Specifies the number of `workers` to boot in clustered mode.
# Workers are forked web server processes. If using threads and workers together
# the concurrency of the application would be max `threads` * `workers`.
# Workers do not work on JRuby or Windows (both of which do not support
# processes).
#
# It is recommended to use the number of available cores as the number of workers.
# The `WEB_CONCURRENCY` environment variable is used to set the number of workers.
require "concurrent"
workers ENV.fetch("WEB_CONCURRENCY", Concurrent.physical_processor_count)

# Preload the application before starting the workers.
preload_app!

# Specifies the `port` that Puma will listen on to receive requests; default is 3000.
port        ENV.fetch("PORT", 3000)

# Specifies the `environment` that Puma will run in.
environment ENV.fetch("RAILS_ENV") { "development" }

# Specifies the `pidfile` that Puma will use.
pidfile ENV.fetch("PIDFILE") { "tmp/pids/server.pid" }

# Allow puma to be restarted by `bin/rails restart` command.
plugin :tmp_restart