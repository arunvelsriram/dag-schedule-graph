FROM node:15.3.0-alpine as ui-assets-builder

WORKDIR /opt/dag-schedule-graph

COPY ./package.json ./
COPY ./package-lock.json ./
RUN npm install
COPY ./ ./
RUN npm run build:production

FROM apache/airflow:1.10.14-python3.7

WORKDIR /opt/dag-schedule-graph

COPY ./ ./
COPY --from=ui-assets-builder /opt/dag-schedule-graph/dag_schedule_graph/static/dist ./dag_schedule_graph/static/dist
RUN pip install .

ENTRYPOINT ["./scripts/docker/airflow-entrypoint.sh"]
