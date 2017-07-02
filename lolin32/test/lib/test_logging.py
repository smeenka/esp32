# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === library  tests  ===
# ------------------------------------------------------------
import logging


logging.setGlobal(logging.TRACE)
log = logging.getlogger("test")
log.debug("Test message (not printed): %d (%s)", 100, "INFO / global: TRACE")
log.info("Test message2 (printed): %d (%s)", 100, "INFO / global: TRACE")

log.setLevel(logging.DEBUG)
log.info("lower level of test: %d (%s)", 100, "DEBUG / global: TRACE")
log.debug("Test message (printed): %d (%s)", 100, "DEBUG / global: TRACE")

logging.setGlobal(logging.WARNING)
log.warn( "raise global level: %d (%s)", 100, "DEBUG / global: WARN"  )
log.debug("Test message (not printed): %d(%s)", 100, "DEBUG / global: WARN")

log.error("xxx" )
